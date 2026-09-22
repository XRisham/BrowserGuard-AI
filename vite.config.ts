import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL(".", import.meta.url));
export default defineConfig({ plugins:[react()], build:{ outDir:"dist", emptyOutDir:true, rollupOptions:{ input:{ popup:resolve(root,"popup.html"), dashboard:resolve(root,"dashboard.html"), settings:resolve(root,"settings.html"), onboarding:resolve(root,"onboarding.html"), block:resolve(root,"block.html"), background:resolve(root,"src/background/service-worker.ts"), content:resolve(root,"src/content/content.ts") }, output:{ entryFileNames:"assets/[name].js" } } }, test:{ environment:"jsdom" } });
