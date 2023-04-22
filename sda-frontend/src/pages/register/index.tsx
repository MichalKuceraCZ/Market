import {TitleWrapper} from "@/components/TitleWrapper";
import {Button, PasswordInput, TextInput} from "@mantine/core";
import {useRouter} from "next/router";
import {useMutation} from "react-query";
import {useForm} from "@mantine/form";
import axios from "axios";

type FormValues = {
    username: string;
    firstName: string;
    lastName: string;
    email: string;
    password: string;
    repeatPassword: string;
};

function camelToSnake(obj: { [key: string]: string }) {
    const snakeObj: { [key: string]: string } = {};

    for (const [key, value] of Object.entries(obj)) {
        const snakeKey = key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
        snakeObj[snakeKey] = value;
    }

    return snakeObj;
}

export default function RegisterPage() {
    const router = useRouter();

    const { mutate, isLoading, error } = useMutation("registerUser", registerUser, {
        onSuccess: async () => {
            await router.push("/login");
        },
    });

    const form = useForm<FormValues>({
        initialValues: { username: "", email: "", firstName: "", lastName: "", repeatPassword: "", password: "" },

        // functions will be used to validate values at corresponding key
        validate: {
            username: (value) => (value.length < 2 ? "Username must have at least 2 characters" : null),
            email: (value) =>
                !/\S+@\S+\.\S+/.test(value) ? "Please enter a valid email address" : null,
            firstName: (value) => (value.length < 2 ? "Name must have at least 2 characters" : null),
            lastName: (value) => (value.length < 2 ? "Name must have at least 2 characters" : null),
            password: (value) => (value.length < 8 ? "Name must have at least 8 characters" : null),
            repeatPassword: (value, values) =>
                value !== values.password ? "Passwords do not match" : null,
        },
    });

    async function registerUser(formData: FormValues) {
        const { repeatPassword, ...others } = formData;

        const { data } = await axios.post("http://localhost:8000/api/v1/users", camelToSnake(others));
        return data;
    }

    function onSubmit(formData: FormValues) {
        mutate(formData);
    }

    return (
        <div>
            <TitleWrapper title={"Register"}/>

             <form className={"flex flex-col gap-4"} onSubmit={form.onSubmit(onSubmit)}>
                <TextInput
                    label={"Username"}
                    placeholder={"Username"}
                    {...form.getInputProps("username")}
                />

                <TextInput
                    label={"First name"}
                    placeholder={"First name"}
                    {...form.getInputProps("firstName")}
                />

                <TextInput
                    label={"Last name"}
                    placeholder={"Last name"}
                    {...form.getInputProps("lastName")}
                />

                <TextInput
                    label={"Email"}
                    placeholder={"Email"}
                    type={"email"}
                    {...form.getInputProps("email")}
                />

                <PasswordInput
                    label={"Password"}
                    placeholder={"Password"}
                    {...form.getInputProps("password")}
                />

                <PasswordInput
                    label={"Repeat password"}
                    placeholder={"Repeat password"}
                    {...form.getInputProps("repeatPassword")}
                />

                <Button type={"submit"} variant={"outline"} disabled={isLoading || (!form.isValid && form.isTouched)}>Submit</Button>
            </form>
        </div>
    );
}