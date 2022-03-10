import React, { useEffect, useState } from 'react'
// mui


import { MenuItem, Select, InputLabel, FormControl, IconButton, Divider } from '@mui/material';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';

import ResistanceEdit from './ResistanceEdit';
import CardioEdit from './CardioEdit';

import axiosInstance from '../../axios'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import ExerciseEditDetail from './ExerciseDetailEdit';

export default function ExerciseItem({ data, workoutID, updateWorkout }) {
    const queryClient = useQueryClient()
    // handles logic for exercise editing

    const [exerciseData, setExerciseData] = useState(data)
    const [openExerciseEditor, setopenExerciseEditor] = useState(false)
    // const [errorMessage, setErrorMessage] = useState(null)
    const updateTextFields = (e) => {
        setExerciseData({
            ...exerciseData,
            [e.target.id]: e.target.value,
        });

    };

    const updateSelectFields = (e) => {
        setExerciseData({
            ...exerciseData,
            [e.target.name]: e.target.value.trim(),
        });
    }

    const updateCheckedFields = (e) => {
        setExerciseData({
            ...exerciseData,
            [e.target.id]: e.target.checked,
        });
    }

    const removeExercise = useMutation(exercise => {
        return axiosInstance.delete(`workout/${workoutID}/exercise/${data.id}/`, exercise)
    }, {
        onSuccess: () => { queryClient.invalidateQueries("workout_exercises") }
    })

    const handleRemoveExercise = () => {
        removeExercise.mutate()
    }

    useEffect(() => {
        updateWorkout(exerciseData)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [exerciseData])


    const [showResistanceEdit, setShowResistanceEdit] = useState(true)

    const handleSwitch = (value) => {
        setShowResistanceEdit(value)
        setExerciseData({ ...exerciseData, resistance_view: value })
    }


    return (
        <>
            <ExerciseEditDetail
                handleClose={() => setopenExerciseEditor(false)}
                updateTextFields={updateTextFields}
                updateSelectFields={updateSelectFields}
                updateCheckedFields={updateCheckedFields}
                data={exerciseData}
                open={openExerciseEditor}
            />
            {showResistanceEdit ?
                <ResistanceEdit data={exerciseData} handleSwitch={handleSwitch}
                    updateTextFields={updateTextFields}
                    updateSelectFields={updateSelectFields}
                    handleRemoveExercise={handleRemoveExercise}
                    updateCheckedFields={updateCheckedFields}
                    openExerciseEditor={() => setopenExerciseEditor(true)}
                /> :
                <CardioEdit data={exerciseData} handleSwitch={handleSwitch}
                    updateTextFields={updateTextFields}
                    updateSelectFields={updateSelectFields}
                    handleRemoveExercise={handleRemoveExercise}
                    updateCheckedFields={updateCheckedFields} />}
        </>
    )
}