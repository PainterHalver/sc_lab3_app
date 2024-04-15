import { useEffect, useState } from "react"
import { ImDownload3 } from "react-icons/im";
import { BASE_URL } from "../const";

export default function CSVList() {
    const [loading, setLoading] = useState(false);
    const [csvs, setCsvs] = useState([]);

    const getCSVFiles = async () => {
        try {
            setLoading(true)
            const response = await fetch(`${BASE_URL}/api/csv`);
            const data = await response.json();
            setCsvs(data);
        } catch (error) {
            console.log("GET CSV FILES ERROR:", error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        getCSVFiles();
    }, [])

    return <div className="flex flex-col items-center gap-5">
        <button className="btn btn-lg btn-primary disabled:bg-primary disabled:text-white" onClick={getCSVFiles} disabled={loading}>
            Reload
        </button>
        {loading && <span className="loading loading-spinner"></span>}

        <table className="w-full text-sm text-left rtl:text-right">
            <thead className="uppercase text-md bg-[--bg-table-header]">
                <tr>
                    <th scope="col" className="px-6 py-3">
                        ID
                    </th>
                    <th scope="col" className="px-6 py-3">
                        File Name
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Generated At
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Download
                    </th>
                </tr>
            </thead>
            <tbody>
                {csvs.map((csv) => (
                    <tr key={csv["id"]} className="bg-[--bg-secondary] border-b border-border hover:bg-[#1c1f2699]">
                        <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap">
                            {csv["id"]}
                        </th>
                        <td className="px-6 py-3">{csv["filename"]}</td>
                        <td className="px-6 py-3">{csv["generated_at"]}</td>
                        <td className="px-6 py-3">
                            <a
                                className="btn btn-success btn-sm"
                                href={`${BASE_URL}/api/csv/${csv["id"]}`}
                            >
                                <ImDownload3 />
                            </a>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}