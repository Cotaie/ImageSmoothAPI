import {addFileNameSuffix, getQueryParams, imageHeaders} from "./utils.ts"

export const sendResponse = async (request: Request): Promise<Response> => {
    const queryParams = getQueryParams(request)
    const outputFileName = `${addFileNameSuffix(queryParams.image_name)(queryParams.smoothing_type)}`
    const image = await Deno.readFile(`./render_image/${outputFileName}`)
    await Deno.remove(`./render_image/${outputFileName}`)
    const headers = new Headers(imageHeaders)
    headers.set("Content-Disposition", `inline; filename="${outputFileName}"`);
    return new Response(image, {
        status: 200,
        headers: headers
    })
}

export const sendResponse2 = (location: string) => async (req: Request): Promise<Response> => {
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