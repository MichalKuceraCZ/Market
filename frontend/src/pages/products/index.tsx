type Category = {
    id: number;
    name: string;
};
// array = list
const categories: Category[] = [
    {
        id: 1,
        name: "fruit",
    },
    {
        id: 2,
        name: "vegetables",
    },
];
export default function ProductsPage() {
    return (
        <div>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                </tr>
                </thead>
                <tbody>
                {categories.map((category) => (
                    <tr key={category.id}>
                        <td>{category.id}</td>
                        <td>{category.name}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            <ul>
                {categories.map((category) => (
                    <li key={category.id}>{category.name}</li>
                ))}
            </ul>
        </div>
    );
}
