import { Middleware, Handler } from "./types.ts"

export type Middleware1 = (request: Request) => Promise<unknown>

export interface Route {
    pathname: string
    middlewares?: Array<Middleware> | Middleware1
    handler: Handler
}