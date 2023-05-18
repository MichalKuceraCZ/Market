const session = false;

export async function protectAuthRoute(context: never) {
    // const session = await getSession(context);
    if (!session) {
        return {
            redirect: {
                destination: "/login",
                permanent: false,
            },
        };
    }
    return { props: {} };
}


export async function protectRoute(context: never) {
    // const session = await getSession(context);
    if (session) {
        return {
            redirect: {
                destination: "/todos",
                permanent: false,
            },
        };
    }

    return { props: {} };
}
