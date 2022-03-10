import React, { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'react-router-dom';
// mui
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Pagination from '@mui/material/Pagination';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import Fab from '@mui/material/Fab';
// components
import WorkoutExercises from './UserExercises';
// components
// import WorkoutSearchBar from '../page/WorkoutSearchBar';
// import SetListItem from './SetListItem';
// import AddSetListItem from './AddSetListItem';
// import EmptyPage from '../extra/EmptyPage';
// import CreateSetInput from './SetInput';
// import AlertComponent from '../extra/AlertComponent';
// import SimpleAlertComponent from '../extra/SimpleAlertComponent';
// import MultipleSelect from '../extra/MultiSelect';

// view page to edit a user workout
function WorkoutBuilder(any) {
    const params = useParams()


    return (
        <React.Fragment>

            <Box sx={{ flexGrow: 4, margin: 4 }}>
                <Grid container spacing={12} justifyContent="center" sx={{ maxHeight: "80vh" }}>
                    <Grid item xs>
                        {/* search function to add new workouts */}
                        <Paper elevation={3} sx={{ bgcolor: "lightgrey", minHeight: "50vh", padding: 1 }}>

                        </Paper>
                    </Grid>
                    <Grid item md>
                        {/* area to see current workouts */}
                        <Paper elevation={3} sx={{ bgcolor: "darkgrey", minHeight: "50vh", padding: 1 }}>
                            <WorkoutExercises workoutID={params.uuid} />
                        </Paper>
                    </Grid>

                </Grid>


            </Box>
        </React.Fragment>

    )
}

export default WorkoutBuilder