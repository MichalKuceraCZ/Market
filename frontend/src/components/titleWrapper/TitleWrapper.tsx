import { Title } from "@mantine/core";

type Props = {
    title: string;
};

export function TitleWrapper({ title }: Props) {
    return (
        <Title className={"flex justify-center pb-6"}>{title}</Title>
    );
}
