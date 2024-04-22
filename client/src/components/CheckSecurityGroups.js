import { useState } from "react";
import { BASE_URL } from "../const";

export default function CheckSecurityGroups() {
    const [securityGroups, setSecurityGroups] = useState([]);
    const [csv, setCsv] = useState(null);
    const [loading, setLoading] = useState(false);

    const checkSecurityGroups = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${BASE_URL}/api/security_groups`, {
                method: "POST"
            });
            const data = await response.json();
            const sortedSecurityGroups = data.security_groups.sort((a, b) => b["Annotations"].length - a["Annotations"].length)
            setCsv(data.csv);
            setSecurityGroups(sortedSecurityGroups);
        } catch (error) {
            console.log("CHECK SECURITY GROUPS ERROR:", error)
        } finally {
            setLoading(false)
        }
    }

    return <div className="flex flex-col items-center gap-5">
        <button className="btn btn-lg btn-primary disabled:bg-primary disabled:text-white" onClick={checkSecurityGroups} disabled={loading}>
            {loading && <span className="loading loading-spinner"></span>} Check
        </button>
        {csv &&
            (<p>Last Check: <a href={`${BASE_URL}/api/csv/${csv.id}`}>{csv.filename}</a> generated at {csv.generated_at}</p>)
        }
        <table className="w-full text-sm text-left rtl:text-right">
            <thead className="uppercase text-md bg-[--bg-table-header]">
                <tr>
                    <th scope="col" className="px-6 py-3">
                        Group ID
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Group Name
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Description
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Compliance Type
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Annotations
                    </th>
                </tr>
            </thead>
            <tbody>
                {securityGroups.map((sg) => (
                    <tr key={sg["GroupId"]} className="bg-[--bg-secondary] border-b border-border hover:bg-[#1c1f2699]">
                        <th scope="row" className="px-6 py-4 font-medium whitespace-nowrap">
                            {sg["GroupId"]}
                        </th>
                        <td className="px-6 py-3">{sg["GroupName"]}</td>
                        <td className="px-6 py-3">{sg["Description"]}</td>
                        <td className="px-6 py-3">
                            <div className={`badge ${sg["ComplianceType"] === "COMPLIANT" ? 'badge-success' : 'badge-error'}`}>
                                {sg["ComplianceType"]}
                            </div>
                        </td>
                        <td className="px-6 py-3">
                            {sg["Annotations"].map((annotation) => (
                                <p className="text-sm" key={annotation}>{annotation}</p>
                            ))}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

// {
//     "csv": {
//       "filename": "security_groups/sg-report-1713168852.csv",
//       "generated_at": "Mon, 15 Apr 2024 08:14:12 GMT",
//       "id": 4
//     },
//     "security_groups": [
//       {
//         "Annotations": [
//           "No tcp ['22'] port is authorized to be open, according to the authorizedTcpPorts parameter."
//         ],
//         "ComplianceType": "NON_COMPLIANT",
//         "Description": "default VPC security group",
//         "GroupId": "sg-05df27e56b0a450da",
//         "GroupName": "default",
//         "IpPermissions": [
//           {
//             "FromPort": 22,
//             "IpProtocol": "tcp",
//             "IpRanges": [
//               {
//                 "CidrIp": "0.0.0.0/0"
//               }
//             ],
//             "Ipv6Ranges": [],
//             "PrefixListIds": [],
//             "ToPort": 22,
//             "UserIdGroupPairs": []
//           }
//         ],
//         "IpPermissionsEgress": [
//           {
//             "IpProtocol": "-1",
//             "IpRanges": [
//               {
//                 "CidrIp": "0.0.0.0/0"
//               }
//             ],
//             "Ipv6Ranges": [],
//             "PrefixListIds": [],
//             "UserIdGroupPairs": []
//           }
//         ],
//         "OwnerId": "008189915245",
//         "VpcId": "vpc-0da23ba6547b406ba"
//       },
//       {
//         "Annotations": [
//           "This Amazon EC2 security group is not associated with an EC2 instance or an ENI.",
//           "No tcp ['22', '9001'] port is authorized to be open, according to the authorizedTcpPorts parameter."
//         ],
//         "ComplianceType": "NON_COMPLIANT",
//         "Description": "launch-wizard-1 created 2023-12-04T02:21:05.622Z",
//         "GroupId": "sg-0e26a71aac1bd9c1c",
//         "GroupName": "launch-wizard-1",
//         "IpPermissions": [
//           {
//             "FromPort": 22,
//             "IpProtocol": "tcp",
//             "IpRanges": [
//               {
//                 "CidrIp": "0.0.0.0/0"
//               }
//             ],
//             "Ipv6Ranges": [],
//             "PrefixListIds": [],
//             "ToPort": 22,
//             "UserIdGroupPairs": []
//           },
//           {
//             "FromPort": 9001,
//             "IpProtocol": "tcp",
//             "IpRanges": [
//               {
//                 "CidrIp": "0.0.0.0/0",
//                 "Description": "allow 9001"
//               }
//             ],
//             "Ipv6Ranges": [],
//             "PrefixListIds": [],
//             "ToPort": 9001,
//             "UserIdGroupPairs": []
//           }
//         ],
//         "IpPermissionsEgress": [
//           {
//             "IpProtocol": "-1",
//             "IpRanges": [
//               {
//                 "CidrIp": "0.0.0.0/0"
//               }
//             ],
//             "Ipv6Ranges": [],
//             "PrefixListIds": [],
//             "UserIdGroupPairs": []
//           }
//         ],
//         "OwnerId": "008189915245",
//         "VpcId": "vpc-0da23ba6547b406ba"
//       }
//     ],
//     "status": "success"
//   }