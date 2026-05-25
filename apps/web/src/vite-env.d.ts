/// <reference types="vite/client" />

declare module "@mlc-ai/web-llm" {
  export const prebuiltAppConfig: any;
  export function CreateMLCEngine(modelId: string, options?: any): Promise<any>;
}
