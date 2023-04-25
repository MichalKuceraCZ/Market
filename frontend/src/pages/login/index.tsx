import axios from "axios";
import { useRouter } from "next/router";
import { useMutation } from "react-query";

import { AuthLayout } from "@/layouts/authLayout/AuthLayout";
import { TitleWrapper } from "@/components/titleWrapper/TitleWrapper";
import { protectRoute } from "@/protectedRoutes";
import { camelToSnake } from "@/utils";
import { useForm } from "@mantine/form";
import { Button, PasswordInput, TextInput } from "@mantine/core";

type FormValues = {
    username: string;
    password: string;
};

export default function LoginPage() {
    const router = useRouter();


    const form = useForm<FormValues>({
        initialValues: { username: "", password: "" },

        // functions will be used to validate values at corresponding key
        validate: {
            username: (value) => (value.length < 2 ? "Username must have at least 2 characters" : null),
            password: (value) => (value.length < 8 ? "Name must have at least 8 characters" : null),
        },
    });

    const { mutate, isLoading, error } = useMutation("loginUser", loginUser, {
        onSuccess: async () => {
            await router.push("/todos");
        },
    });

    async function loginUser(formData: FormValues) {
        const { data } = await axios.post("http://localhost:8000/api/v1/users/login", camelToSnake(formData));
        return data;
    }

    function onSubmit(formData: FormValues) {
        mutate(formData)
    }


    return (
        <AuthLayout>
            <TitleWrapper title={"Login"}/>

            <form className={"flex flex-col gap-4"} onSubmit={form.onSubmit(onSubmit)}>
                <TextInput
                    label={"Username"}
                    placeholder={"Username"}
                    {...form.getInputProps("username")}
                />

                <PasswordInput
                    label={"Password"}
                    placeholder={"Password"}
                    {...form.getInputProps("password")}
                />

                <Button type={"submit"} variant={"outline"} disabled={isLoading || (!form.isValid && form.isTouched)}>Submit</Button>
            </form>
        </AuthLayout>
    );
}

export const getServerSideProps = protectRoute;