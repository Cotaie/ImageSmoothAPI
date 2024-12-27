const textHtmlHeaders = new Headers({"Content-Type": "text/html"})
const imageHeaders = new Headers({"Content-Type": "image/*"})

const getQueryParams = (request: Request): Map<string,string> => {
    const url = new URL(request.url)
    const queryParams = url.searchParams
    const args = new Map<string, string>()
    queryParams.forEach((value, key) => args.set(key, value))
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

        const queryParamsValues = ((queryParams: Map<string,string>) => {
            const queryParamsValues = [] as Array<string>
            queryParamsValues[0] = queryParams.get('image_name') ?? ""
            queryParamsValues[1] = queryParams.get('smoothing_type')  ?? ""
            queryParamsValues[2] = queryParams.get('kernel_size') ?? ""
            queryParamsValues[3] = queryParams.get('signal_color') ?? queryParams.get('convolution_mode') ?? queryParams.get('border_mode') ?? ""
            queryParamsValues[4] = queryParams.get('sigma_space') ?? queryParams.get('median_type') ?? ""
            return queryParamsValues
        })(queryParams)

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
        headers.set("Content-Disposition", `inline; filename="${queryParams.get('image_name')}"`);
        headers.set("Content-Type", `image/*`);
        //headers.set("X-Time-Taken", `${timeTaken}`)
        return new Response(stdout, {
            status: 200,
            headers: headers
        })
}