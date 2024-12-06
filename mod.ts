import { Route } from "./imports/interfaces.ts"
import { getInputImage, removeInputImage, doPythonScript, doPythonScript1, doPythonScript2 } from "./middlewares.ts"
import { Middleware } from "./imports/types.ts"
import { aliveCheck, sendResponseError } from "./utils.ts"
import { sendResponse, sendResponse2 } from "./handlers.ts"

const PORT = 9009

// const getMiddlewares = (middleware: Middleware ) => [(request: Request) => getInputImage(request),
//                                                       middleware,
//                                                     (request: Request) => removeInputImage(request)]

const routes: Array<Route> = [
    // {pathname: "/", handler: () => aliveCheck()},
    // {pathname: "/opencv", middlewares: getMiddlewares((request: Request) => doPythonScript(request)('./scripts/process_opencv.py')), handler: (request: Request) => sendResponse(request)},
    // {pathname: "/convolve1d", middlewares: getMiddlewares((request: Request) => doPythonScript(request)('./scripts/process_convolve1d.py')), handler: (request: Request) => sendResponse(request)},
    // {pathname: "/convolve2d", middlewares: getMiddlewares((request: Request) => doPythonScript(request)('./scripts/process_convolve2d.py')), handler: (request: Request) => sendResponse(request)},
    // {pathname: "/test", middlewares: getMiddlewares((request: Request) => doPythonScript(request)('./scripts/test.py')), handler: (request: Request) => sendResponse(request)},
    //{pathname: "/opencv1", middlewares: [(request: Request) => doPythonScript1(request)('./scripts/process_opencv1.py')], handler: (request: Request) => sendResponse(request)},
    {pathname: "/convolve1d", handler: (request: Request) => sendResponse2('./scripts/process_convolve1d2.py')(request)},
    {pathname: "/opencv2", handler: (request: Request) => sendResponse2("./scripts/process_opencv2.py")(request)}
    //{pathname: "/opencv2", handler: (request: Request) => sendResponse2("./scripts/testt.py")(request)}
]

// const router = async (request: Request): Promise<Response> => {
//     const hasPath = (route: Route) => route.pathname === (new URL(request.url).pathname)
//     const route = routes.find(hasPath)ß
//     const middlewares = route?.middlewares ?? []
//     try {
//         for (const middleware of middlewares) {
//         await middleware(request)
//         }
//         return await route?.handler(request) ?? sendResponseError(404, "Path Not Found")();
//     } catch(error) {
//         console.log("ERRR: ", error)
//         return sendResponseError(500, (<Error>error).message)()
//     }
// }

const router = async (request: Request): Promise<Response> => {
    const hasPath = (route: Route) => route.pathname === (new URL(request.url).pathname)
    const route = routes.find(hasPath)
    //const middlewares = route?.middlewares ?? []
    try {
        return await route?.handler(request) ?? sendResponseError(404, "Path Not Found")();
    } catch(error) {
        console.log("ERRR: ", error)
        return sendResponseError(500, (<Error>error).message)()
    }
}

Deno.serve({port: PORT}, (req) => router(req));