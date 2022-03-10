import React, { useEffect, useState } from 'react'
// mui
import Card from '@mui/material/Card';
import DeleteIcon from '@mui/icons-material/Delete';

import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';
import { MenuItem, Select, InputLabel, FormControl, IconButton, Divider } from '@mui/material';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';

import EditIcon from '@mui/icons-material/Edit';
import ResistanceEdit from './ResistanceEdit';
import CardioEdit from './CardioEdit';

export default function ExerciseItem({ data }) {
    const [exerciseData, setExerciseData] = useState(data)
    // const [errorMessage, setErrorMessage] = useState(null)

    const updateTextFields = (e) => {
        // setExerciseData({
        //     ...exerciseData,
        //     [e.target.id]: e.target.value.trim(),
        // });
        console.log(e.target.value)
    };

    const [showResistanceEdit, setShowResistanceEdit] = useState(true)

    const handleSwitch = (value) => {
        setShowResistanceEdit(value)
    }


    return (
        <>
            {showResistanceEdit ?
                <ResistanceEdit data={data} handleSwitch={handleSwitch}
                    updateTextFields={updateTextFields} /> :
                <CardioEdit data={data} handleSwitch={handleSwitch}
                    updateTextFields={updateTextFields} />}
        </>
    )
}