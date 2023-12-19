"use client"

import { useEffect, useState } from "react"
import Image from "next/image"
import { ColorRing } from "react-loader-spinner"
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

const Rows = (props: { rows: Row[] }) => {
    const [colours, setColours] = useState<ColourMap>(defaultColourMap)
    return (
        <div className="flex flex-col w-full">
            {props.rows.map((r) => (
                <Row
                    key={r.actual_datetime.getTime()}
                    row={r}
                    colourMap={colours}
                />
            ))}
        </div>
    )
}

const Home = () => {
    const [isLoading, setLoading] = useState(true)
    const [rows, setRows] = useState<Row[]>([])
    useEffect(() => {
        getRows(setRows, setLoading)
    }, [])
    return (
        <main>
            <div className="w-mobileContent tablet:w-tabletContent desktop:w-content m-auto flex justify-center">
                {isLoading ? (
                    <ColorRing
                        visible={true}
                        height="80"
                        width="80"
                        ariaLabel="blocks-loading"
                        wrapperStyle={{}}
                        wrapperClass="blocks-wrapper"
                        colors={[
                            "#0000ff",
                            "#0000ff",
                            "#0000ff",
                            "#0000ff",
                            "#0000ff",
                        ]}
                    />
                ) : (
                    <Rows rows={rows} />
                )}
            </div>
        </main>
    )
}

export default Home
