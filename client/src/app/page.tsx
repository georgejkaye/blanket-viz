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
    let padding = props.row.is_day ? "h-10 py-3" : "h-8 py-2"
    let svgPath = props.row.is_day ? sun : moon
    let svgAlt = props.row.is_day ? "Sun" : "Moon"
    const [isHover, setHover] = useState(false)
    return (
        <div className="flex flex-row align-center content-center leading-none">
            {}
            <div
                className={`flex flex-row flex-1 ${colour.code} text-center ${padding} mx-4 px-4`}
                onMouseOver={(e) => setHover(true)}
                onMouseLeave={(e) => setHover(false)}
            >
                {isHover ? (
                    <>
                        <div>{getRowDateString(props.row)}</div>
                        <Image
                            src={svgPath}
                            width={15}
                            height={15}
                            alt={svgAlt}
                            className={"ml-4"}
                        />
                        <div className="flex-1">{colour.name}</div>
                        <div className={`text-left`}>
                            {props.row.temperature}
                        </div>
                    </>
                ) : (
                    ""
                )}
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
