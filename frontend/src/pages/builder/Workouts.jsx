import React from 'react';
import { useQuery } from 'react-query'
import axiosInstance from '../../axios';
// mui
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
// components
import Loading from '../../components/Loading';
import WorkoutItem from './WorkoutItem';

export default function Workouts() {

    const { isLoading, error, data } = useQuery("workouts", () =>
        axiosInstance.get("/workouts/").then((res) => {
            return res.data.results
        }))

    if (isLoading) return <Loading />

    if (error) return 'An error has occurred: ' + error.message

    return (
        <List>
            {data.map((workout) => {
                return (
                    <React.Fragment key={workout.id}>
                        <WorkoutItem details={workout} handleDelete={() => console.log("delete workout please")} />
                        <Divider />
                    </React.Fragment>
                )
            })}
        </List>
    )
}