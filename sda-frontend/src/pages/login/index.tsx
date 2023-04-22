// class -> className
import Link from "next/link";

import {TextInput, PasswordInput, Button} from "@mantine/core";

import {TitleWrapper} from "@/components/TitleWrapper";

export default function LoginPage() {
    return (
        <div>
            <TitleWrapper title={"Login"}/>

            <form className={"flex flex-col gap-4"}>
                <TextInput
                    label={"Username"}
                    placeholder={"Username"}
                />

                <PasswordInput
                    label={"Password"}
                    placeholder={"Password"}
                />

                <Button variant={"outline"} type={"submit"}>Submit</Button>

                <Link href={"/register"}>Register</Link>
            </form>
        </div>
    );
}