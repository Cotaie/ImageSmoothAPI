
import { extname, basename } from "path"


type QueryParamsType = { [key: string]: string }

export const textHtmlHeaders = new Headers({"Content-Type": "text/html"})
export const imageHeaders = new Headers({"Content-Type": "image/*"})

export const aliveCheck = (): Response => 
    new Response(JSON.stringify({ message: "Alive check"} ), { status: 200, headers: textHtmlHeaders })

export const addFileNameSuffix = (filename: string) => 
    (suffix: string): string => `${basename(filename, extname(filename))}_${suffix}${extname(filename)}`

export const getQueryParams = (request: Request): QueryParamsType => {
    const url = new URL(request.url)
    const queryParams = url.searchParams
    const args: QueryParamsType = {}
    queryParams.forEach((value, key) => args[key] = value)
    console.log("ARGS: ", args)
    return args
}

export const sendResponseError = (code: number, error: string,) => 
    () => new Response(JSON.stringify({messagee: error}), { status: code, headers: textHtmlHeaders })
