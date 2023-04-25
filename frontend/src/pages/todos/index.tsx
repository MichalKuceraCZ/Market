import axios from "axios";
import { useQuery } from "react-query";

import { Layout } from "@/layouts/layout/layout";
import { TitleWrapper } from "@/components/titleWrapper/TitleWrapper";

import { config } from "../../../config";
import { protectAuthRoute } from "@/protectedRoutes";

export default function TodosPage() {
    const { data: todos, isLoading, error: someDataError } = useQuery("todos", getTodos);

    console.log(todos);

    async function getTodos() {
        const { data } = await axios.get(`${config}/api/v1/todos`)
        return data;
    }

    return (
        <Layout>
            <TitleWrapper title={"Todos"}/>
        </Layout>
    );
}

export const getServerSideProps = protectAuthRoute;
