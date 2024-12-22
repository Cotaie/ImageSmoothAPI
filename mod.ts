import { sendResponse, sendManualResponse } from "./handlers.ts"


const PORT = 9010

interface Route {
    pathname: string
    handler: (request: Request) => Promise<Response> | Response
}

const routes: Array<Route> = [
    {pathname: "/", handler: (_request: Request) => sendManualResponse(200, "Alive Check")()},
    {pathname: "/convolve1d", handler: (request: Request) => sendResponse('./scripts/process_convolve1d.py')(request)},
    {pathname: "/convolve2d", handler: (request: Request) => sendResponse('./scripts/process_convolve2d.py')(request)},
    {pathname: "/opencv", handler: (request: Request) => sendResponse("./scripts/process_opencv.py")(request)},
    {pathname: "/median", handler: (request: Request) => sendResponse("./scripts/process_median.py")(request)},
    {pathname: "/bilateral", handler: (request: Request) => sendResponse("./scripts/process_bilateral.py")(request)},
]

const router = async (request: Request): Promise<Response> => {
    const hasPath = (route: Route) => route.pathname === (new URL(request.url).pathname)
    const route = routes.find(hasPath)
    try {
        return await route?.handler(request) ?? sendManualResponse(404, "Path Not Found")();
    } catch(error) {
        console.log("ERRR: ", error)
        return sendManualResponse(500, (<Error>error).message)()
    }
}

Deno.serve({port: PORT}, (req) => router(req));