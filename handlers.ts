type QueryParamsType = { [key: string]: string }

const textHtmlHeaders = new Headers({"Content-Type": "text/html"})
const imageHeaders = new Headers({"Content-Type": "image/*"})

const getQueryParams = (request: Request): QueryParamsType => {
    const url = new URL(request.url)
    const queryParams = url.searchParams
    const args: QueryParamsType = {}
    queryParams.forEach((value, key) => args[key] = value)
    console.log("ARGS: ", args)
    return args
}

export const sendManualResponse = (code: number, error: string,) => 
    () => new Response(JSON.stringify({messagee: error}), { status: code, headers: textHtmlHeaders })

export const sendResponse = (location: string) => async (req: Request): Promise<Response> => {
        //get image from req
        const formData = await req.formData();
        const file = <File>formData.get("image");
        console.log("File:", file)
        const buffer = await file.arrayBuffer();
        const uint8Array = new Uint8Array(buffer);

        const queryParams = getQueryParams(req)
        const queryParamsValues = Object.values(queryParams)
        const command = new Deno.Command("python", { args: [location, ...queryParamsValues], stdin: "piped", stdout: "piped", stderr: "piped" })

        const process = command.spawn();
        if (process.stdin) {
            const writer = process.stdin.getWriter()
            await writer.write(uint8Array)
            await writer.close()
        }

        const output = await process.output()
        console.log("SRDERR: ", process.stderr)
        const stdout = output.stdout
        const headers = new Headers(imageHeaders)
        headers.set("Content-Disposition", `inline; filename="${queryParams.image_name}"`);
        headers.set("Content-Type", `image/*`);
        //headers.set("X-Time-Taken", `${timeTaken}`)
        return new Response(stdout, {
            status: 200,
            headers: headers
        })
}