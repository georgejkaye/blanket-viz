"use client"

import { useEffect, useState } from "react"
import Image from "next/image"
import {
    ColourMap,
    Row,
    defaultColourMap,
    getColour,
    getRowDateString,
} from "./structs"
import { getRows } from "./api"
import sun from "../../public/sun.svg"
import moon from "../../public/moon.svg"

const Row = (props: { row: Row; colourMap: ColourMap }) => {
    let colour = getColour(props.row.temperature, props.colourMap)
    let padding = props.row.is_day ? "py-6" : "py-2"
    let svgPath = props.row.is_day ? sun : moon
    let svgAlt = props.row.is_day ? "Sun" : "Moon"
    return (
        <div className="flex flex-row align-center content-center leading-none">
            <div className={`w-24 ${padding} mx-2`}>
                {getRowDateString(props.row)}
            </div>
            <Image src={svgPath} width={15} height={15} alt={svgAlt} />
            <div
                className={`flex-1 ${colour.code} text-center ${padding} mx-4`}
            >
                {colour.name}
            </div>
            <div className={`w-10 px-2 ${padding} text-left`}>
                {props.row.temperature}
            </div>
        </div>
    )
}

export const Home = () => {
    const [rows, setRows] = useState<Row[]>([])
    const [colours, setColours] = useState<ColourMap>(defaultColourMap)
    useEffect(() => {
        getRows(setRows)
    }, [])
    return (
        <main>
            <div className="w-mobileContent tablet:w-tabletContent desktop:w-content m-auto">
                {rows.map((r) => (
                    <Row row={r} colourMap={colours} />
                ))}
            </div>
        </main>
    )
}

export default Home
