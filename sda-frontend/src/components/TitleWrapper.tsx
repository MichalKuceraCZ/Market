import {Title} from "@mantine/core";

type Props = {
    title: string;
};

export function TitleWrapper({ title }: Props) {
    return (
      <Title className={"flex items-center justify-center mb-6"}>{title}</Title>
    );
}
