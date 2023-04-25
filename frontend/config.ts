const env = process.env.ENV || "development";

export const config = {
    development: {
        api: "http://localhost:8000/",
    },
}[env];
