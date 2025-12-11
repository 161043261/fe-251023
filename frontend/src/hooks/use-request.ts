import { useAuth } from "@clerk/clerk-react";
import snake2camel from "../utils/snake-to-camel";

const getHeaders = (
  token: string,
  isArray = false,
): [string, string][] | Record<string, string> =>
  isArray
    ? [
        ["Content-Type", "application/json"],
        ["Authorization", `Bearer ${token}`],
      ]
    : {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      };

export default function useRequest() {
  const { getToken } = useAuth();

  const makeRequest = async <TResponse>(
    endpoint: string,
    method = "GET",
    body?: string | Record<string, unknown>,
    headers: HeadersInit = {},
  ) => {
    const token = await getToken();
    if (!token) {
      throw new Error("token === null");
    }
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    endpoint = endpoint.replace(/^\/+/, "");
    const rawResp = await fetch(`${serverUrl}/${endpoint}`, {
      headers: Array.isArray(headers)
        ? [...(getHeaders(token, true) as [string, string][]), ...headers]
        : {
            ...(getHeaders(token) as Record<string, string>),
            ...(headers as Record<string, string>),
          },
      ...(body ? { body: JSON.stringify(body) } : {}),
      method,
    });

    if (!rawResp.ok) {
      const err = (await rawResp.json().catch(console.log)) as unknown;
      if (import.meta.env.DEV) {
        console.log("[makeRequest] err:", err);
      }
      const errMessage = JSON.stringify(err);
      if (rawResp.status === 429) {
        throw new Error("Too Many Requests");
      }
      throw new Error(errMessage);
    }
    const resp = snake2camel<TResponse>(await rawResp.json());
    if (import.meta.env.DEV) {
      console.log("[makeRequest] resp:", resp);
    }
    return resp;
  };

  return makeRequest;
}
