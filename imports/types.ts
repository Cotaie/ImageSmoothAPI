export type Middleware = (request: Request) => Promise<void>
export type Handler = ((request: Request) => Promise<Response> | Response) | (() => Response)