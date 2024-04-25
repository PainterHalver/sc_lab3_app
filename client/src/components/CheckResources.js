import { useEffect, useState } from "react";
import { BASE_URL } from "../const";

export default function CheckResources() {
    const [resources, setResources] = useState([]);
    const [csv, setCsv] = useState(null);
    const [loading, setLoading] = useState(false);

    const [startTime, setStartTime] = useState(null);
    const [elapsedTime, setElapsedTime] = useState(0);

    useEffect(() => {
        let interval;
        if (loading) {
            setStartTime(Date.now());
            interval = setInterval(() => {
                setElapsedTime(Date.now() - startTime);
            }, 1000);
        } else {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [loading, startTime]);

    const checkResources = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${BASE_URL}/api/rules`, {
                method: "POST"
            });
            const data = await response.json();
            const sortedResources = data.resources.sort((a, b) => b["annotations"].length - a["annotations"].length)
            setCsv(data.csv);
            setResources(sortedResources);
        } catch (error) {
            console.log("CHECK RESOURCES ERROR:", error)
        } finally {
            setLoading(false)
        }
    }

    return <div className="flex flex-col items-center gap-5">
        <button className="btn btn-lg btn-primary disabled:bg-primary disabled:text-white" onClick={checkResources} disabled={loading}>
            {loading && <span className="loading loading-spinner"></span>} Check
        </button>
        {loading && <p>Elapsed time: {Math.floor(elapsedTime / 1000)} seconds</p>}
        {csv &&
            (<>
                {!loading && <p>Elapsed time: {Math.floor(elapsedTime / 1000)} seconds.</p>}
                <p>Last Check: <a href={`${BASE_URL}/api/csv/${csv.id}`}>{csv.filename}</a> generated at {csv.generated_at}</p>
            </>)
        }
        <table className="w-full text-sm text-left rtl:text-right">
            <thead className="uppercase text-md bg-[--bg-table-header]">
                <tr>
                    <th scope="col" className="px-6 py-3">
                        Resource ID
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Type
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Name
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Tags
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Compliance Status
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Annotations
                    </th>
                </tr>
            </thead>
            <tbody>
                {resources.map((resource) => (
                    <tr key={resource.id} className="bg-[--bg-secondary] border-b border-border hover:bg-[#1c1f2699]">
                        <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap">
                            {resource.id}
                        </th>
                        <td className="px-6 py-3">{resource.type}</td>
                        <td className="px-6 py-3">{resource.name}</td>
                        <td className="px-6 py-3">
                            {Object.entries(resource.tags).map(([key, value]) => (
                                <p className="text-sm" key={key}>{`${key}: ${value}`}</p>
                            ))}
                        </td>
                        <td className="px-6 py-3">
                            <div className={`badge ${resource.status === "COMPLIANT" ? 'badge-success' : 'badge-error'}`}>
                                {resource.status}
                            </div>
                        </td>
                        <td className="px-6 py-3">
                            {resource.annotations.map((annotation) => (
                                <p className="text-sm" key={annotation}>{annotation}</p>
                            ))}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

/*
{
    "csv": {
        "filename": "noncompliant-resources-20240425-145948.csv",
        "generated_at": "Thu, 25 Apr 2024 14:59:48 GMT",
        "id": 4
    },
    "resources": [
        {
            "annotations": [
                "S3 bucket must be encrypted with a KMS key",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "N/A",
            "id": "hip.daohiep.me",
            "name": "hip.daohiep.me",
            "status": "NON_COMPLIANT",
            "tags": {
                "test": "Test"
            },
            "type": "S3Bucket"
        },
        {
            "annotations": [
                "S3 bucket must be encrypted with a KMS key",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "N/A",
            "id": "nazii",
            "name": "nazii",
            "status": "NON_COMPLIANT",
            "tags": {},
            "type": "S3Bucket"
        },
        {
            "annotations": [
                "S3 bucket must be encrypted with a KMS key",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "N/A",
            "id": "sc-lab3-app-bucket",
            "name": "sc-lab3-app-bucket",
            "status": "NON_COMPLIANT",
            "tags": {},
            "type": "S3Bucket"
        },
        {
            "annotations": [
                "S3 bucket must be encrypted with a KMS key",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "N/A",
            "id": "security-group-compliance-logs-bucket",
            "name": "security-group-compliance-logs-bucket",
            "status": "NON_COMPLIANT",
            "tags": {},
            "type": "S3Bucket"
        },
        {
            "annotations": [
                "S3 bucket must be encrypted with a KMS key",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "N/A",
            "id": "starcamp-lab-terraform-state-bucket",
            "name": "starcamp-lab-terraform-state-bucket",
            "status": "NON_COMPLIANT",
            "tags": {},
            "type": "S3Bucket"
        },
        {
            "annotations": [
                "Security group must not have unrestricted ingress rules (0.0.0.0/0)",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "default VPC security group",
            "id": "sg-05df27e56b0a450da",
            "name": "default",
            "status": "NON_COMPLIANT",
            "tags": {},
            "type": "SecurityGroup"
        },
        {
            "annotations": [
                "Security group must not have unrestricted ingress rules (0.0.0.0/0)",
                "Resource must have required tags Group:CyberDevOps and Environment:Development"
            ],
            "description": "launch-wizard-1 created 2023-12-04T02:21:05.622Z",
            "id": "sg-0e26a71aac1bd9c1c",
            "name": "launch-wizard-1",
            "status": "NON_COMPLIANT",
            "tags": {
                "Test": "test-sg-tag"
            },
            "type": "SecurityGroup"
        }
    ],
    "status": "success"
}
*/
