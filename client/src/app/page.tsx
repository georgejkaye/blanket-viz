"use client"

import { Dispatch, SetStateAction, useEffect, useState } from "react"
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

const Row = (props: {
    row: Row
    colourMap: ColourMap
    selected: boolean
    setSelected: (b: boolean) => void
}) => {
    let colour = getColour(props.row.temperature, props.colourMap)
    let padding = props.row.is_day ? "h-10 py-3" : "h-8 py-2"
    let svgPath = props.row.is_day ? sun : moon
    let svgAlt = props.row.is_day ? "Sun" : "Moon"
    const [clicked, setClicked] = useState(false)
    return (
        <div className="flex flex-row align-center content-center leading-none">
            {}
            <div
                className={`flex flex-row flex-1 ${colour.code} text-center ${padding}`}
                onMouseOver={(e) => props.setSelected(true)}
                onMouseLeave={(e) => props.setSelected(false)}
                onClick={(e) => {
                    props.setSelected(!clicked)
                    setClicked(!clicked)
                }}
            >
                {props.selected ? (
                    <div className="w-mobileContent flex flex-row m-auto">
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
                    </div>
                ) : (
                    ""
                )}
            </div>
        </div>
    )
}

const Rows = (props: { rows: Row[] }) => {
    const [colours, setColours] = useState<ColourMap>(defaultColourMap)
    const [selectedRow, setSelectedRow] = useState<Row | undefined>(undefined)
    const toggleSelectedRow = (r: Row, b: boolean) => {
        if (!b && selectedRow === r) {
            setSelectedRow(undefined)
        } else if (b) {
            setSelectedRow(r)
        }
    }
    return (
        <div className="flex flex-col w-full">
            {props.rows.map((r) => (
                <Row
                    key={r.actual_datetime.getTime()}
                    row={r}
                    colourMap={colours}
                    selected={selectedRow === r}
                    setSelected={(b: boolean) => toggleSelectedRow(r, b)}
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
            <div className="w-full flex justify-center">
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
