import { ReactNode } from "react";
import { Container } from "@mantine/core";

import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

type Props = {
    children: ReactNode;
};

export function AuthLayout({ children }: Props) {
    return (
      <Container className={`${inter.className}`}>{children}</Container>
    );
}
