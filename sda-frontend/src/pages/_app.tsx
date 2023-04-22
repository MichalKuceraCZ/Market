import "@/styles/globals.css";
import type {AppProps} from "next/app";
import {MantineProvider} from "@mantine/core";
import {QueryClient, QueryClientProvider} from "react-query";

const queryClient = new QueryClient()


export default function App({Component, pageProps}: AppProps) {
    return (
        <QueryClientProvider client={queryClient}>
            <MantineProvider
                theme={{
                    colorScheme: "dark",
                }}
                withGlobalStyles
                withNormalizeCSS>
                <Component {...pageProps} />
            </MantineProvider>
        </QueryClientProvider>
    );
}
