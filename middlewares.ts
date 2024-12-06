import { getQueryParams } from "./utils.ts"


export const getInputImage = async (req: Request): Promise<void> => {
    try {
        const formData = await req.formData();
        const file = <File>formData.get("image");
        const buffer = await file.arrayBuffer();
        const uint8Array = new Uint8Array(buffer);
        await Deno.writeFile(`./render_image/${file.name}`, uint8Array)
    } catch (error) {
        console.error("Error processing upload:", error);
    }
}

export const removeInputImage = async (request: Request): Promise<void> => {
    try {
        console.log("NAME: ", getQueryParams(request));
        const queryParams = getQueryParams(request)
        await Deno.remove(`./render_image/${queryParams.image_name}`)
    } catch (error) {
        console.error("Error deleting input image", error);
    }
}

export const doPythonScript = (request: Request) => async (location: string) => {
    try {
        const queryParams = Object.values(getQueryParams(request))
        const command = new Deno.Command("python", { args: [location, ...queryParams], stdout: "piped", stderr: "piped" })
        const output = await command.output()
        console.log("Output:", new TextDecoder().decode(output.stdout)); // Python script output
        console.error("Error:", new TextDecoder().decode(output.stderr)); // Any error messages
    } catch (error) {
            console.error(`Error processing using ${location}`, error);
    }
}

export const doPythonScript1 = (req: Request) => async (location: string) => {
    try {
        //get image from req
        const formData = await req.formData();
        const file = <File>formData.get("image");
        const buffer = await file.arrayBuffer();
        const uint8Array = new Uint8Array(buffer);

        const queryParams = Object.values(getQueryParams(req))
        const command = new Deno.Command("python", { args: [location, ...queryParams], stdin: "piped", stdout: "piped", stderr: "piped" })

        const process = command.spawn();
        if (process.stdin) {
            const writer = process.stdin.getWriter()
            await writer.write(uint8Array)
            await writer.close()
        }

        const output = await process.output()
        console.log("Output:", new TextDecoder().decode(output.stdout)); // Python script output
        console.error("Error:", new TextDecoder().decode(output.stderr)); // Any error messages
    } catch (error) {
            console.error(`Error processing using ${location}`, error);
    }
}

export const doPythonScript2 = (req: Request) => async (location: string) => {
    try {
        //get image from req
        const formData = await req.formData();
        const file = <File>formData.get("image");
        const buffer = await file.arrayBuffer();
        const uint8Array = new Uint8Array(buffer);

        const queryParams = Object.values(getQueryParams(req))
        const command = new Deno.Command("python", { args: [location, ...queryParams], stdin: "piped", stdout: "piped", stderr: "piped" })

        const process = command.spawn();
        if (process.stdin) {
            const writer = process.stdin.getWriter()
            await writer.write(uint8Array)
            await writer.close()
        }

        const output = await process.output()
        console.log("Output:::", new TextDecoder().decode(output.stdout)); // Python script output
        console.error("Error:", new TextDecoder().decode(output.stderr)); // Any error messages

        return <Deno.CommandOutput> output


    } catch (error) {
            console.error(`Error processing using ${location}`, error);
            return <unknown>null as Deno.CommandOutput
    }
}
