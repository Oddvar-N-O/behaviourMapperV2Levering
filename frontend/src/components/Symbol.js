import React from 'react'
import './Symbol.css'

function Symbol(props) {
    return (
        <div>
            <p>image: {props.inf.img}</p> 
            <p>Desc: {props.inf.desc}</p>  
        </div>
    )
}

export default Symbol;