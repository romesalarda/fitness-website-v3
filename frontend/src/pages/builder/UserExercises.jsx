
import { useState } from 'react'
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import Fab from '@mui/material/Fab';

import axiosInstance from '../../axios'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import Loading from './../../components/Loading'
import ExerciseInput from './ExerciseInput';

import React from 'react'
import ExerciseItem from './ExerciseItem'

export default function WorkoutExercises({ workoutID }) {
    const queryClient = useQueryClient()
    // fetch initial exercises
    const { isLoading, error, data } = useQuery("workout_exercises", () =>
        axiosInstance.get(`workout/${workoutID}/exercises/`).then((res) => {
            return res.data.results
        }))
    const [workoutExercises, setWorkoutExercises] = useState(data)

    // update exercises
    const updateWorkoutExercises = useMutation(newWorkout => {
        return axiosInstance.put(`workout/${workoutID}/exercises/`, newWorkout)
    }, {
        onSuccess: () => { queryClient.invalidateQueries("workout_exercises") }
    })
    // create and add a new exercise to workout
    const CreateWorkoutExercise = useMutation(newWorkout => {
        return axiosInstance.post(`workout/${workoutID}/exercises/`, newWorkout)
    }, {
        onSuccess: () => {
            queryClient.invalidateQueries("workout_exercises")
        },
        onError: (e) => { console.log("raise error", e.response.data) }
    })

    const handleCreateExercise = (e) => {
        e.preventDefault()
        const data = {
            title: e.target[0].value,
            repetitions: e.target[2].value,
            sets: e.target[4].value,
            weight: e.target[6].value,
            public: e.target[8].checked,
        }
        CreateWorkoutExercise.mutate(data)
    }

    const handleUpdateWorkout = (exercise) => {
        const updated = data.map(e => {
            if (e.id === exercise.id) {
                return exercise
            }
            return e
        })
        setWorkoutExercises(updated)
    }

    const handleSaveWorkoutExercises = () => {
        console.log(workoutExercises)
        updateWorkoutExercises.mutate(workoutExercises)
    }

    // render
    if (isLoading) return <Loading />

    if (error) return 'An error has occurred: ' + error.message

    return (
        <>
            <ExerciseInput handleCreate={handleCreateExercise} />
            {data.map((exercise) => {
                return (
                    <ExerciseItem
                        workoutID={workoutID}
                        data={exercise}
                        key={exercise.id}
                        updateWorkout={handleUpdateWorkout} />
                )
            })}
            <Fab color="success" aria-label="add" sx={{
                position: "fixed", right: "5vh", bottom: "5vh", width: "10vh", height: "10vh"
            }} size="large" onClick={handleSaveWorkoutExercises}>
                Save <SaveAltIcon />
            </Fab>
        </>
    )

}