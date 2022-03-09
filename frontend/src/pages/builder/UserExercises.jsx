
import axiosInstance from '../../axios'
import { useQuery } from 'react-query'
import Loading from './../../components/Loading'

import React from 'react'
import ExerciseItem from './ExerciseItem'

export default function WorkoutExercises({ workoutID }) {
    const { isLoading, error, data } = useQuery("workout_exercises", () =>
        axiosInstance.get(`workout/${workoutID}/exercises/`).then((res) => {
            return res.data.results
        }))

    if (isLoading) return <Loading />

    if (error) return 'An error has occurred: ' + error.message

    return (
        <>
            {data.map((exercise) => {
                return (
                    <ExerciseItem data={exercise} />
                )
            })}
        </>
    )

}