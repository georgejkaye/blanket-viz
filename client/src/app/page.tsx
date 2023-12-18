"use client"

import { useEffect, useState } from "react"
import { Row, getRowDateString } from "./structs"
import { getRows } from "./api"

const Row = (props: { row: Row }) => {
    return (
        <div className="flex flex-row">
            <div className="w-24 p-2">{getRowDateString(props.row)}</div>
            <div className="p-2">{props.row.is_day ? "D" : "N"}</div>
            <div className="w-10 p-2">{props.row.temperature}</div>
        </div>
    )
}

export const Home = () => {
    const [rows, setRows] = useState<Row[]>([])
    useEffect(() => {
        getRows(setRows)
    }, [])
    return (
        <main>
            <div className="w-72 m-auto">
                {rows.map((r) => (
                    <Row row={r} />
                ))}
            </div>
        </main>
    )
}

export default Home
