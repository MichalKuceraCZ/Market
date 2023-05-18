import { ReactNode } from "react";
import { Container } from "@mantine/core";

type Props = {
    children: ReactNode;
};

export function Layout({ children }: Props) {
    return (
        <Container>{children}</Container>
    );
}
