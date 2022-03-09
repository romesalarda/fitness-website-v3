import React, { useEffect, useState } from 'react'
// mui
import Card from '@mui/material/Card';
import DeleteIcon from '@mui/icons-material/Delete';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';

export default function ExerciseItem({ data }) {
    const [exerciseData, setExerciseData] = useState(data)
    // const [errorMessage, setErrorMessage] = useState(null)

    const updateExercise = (e) => {
        setExerciseData({
            ...exerciseData,
            [e.target.id]: e.target.value.trim(),
        });
    };


    return (
        <Card sx={{ minWidth: 275, bgcolor: "lightgrey", margin: 2 }} variant="outlined">
            <CardContent>
                <TextField
                    id="title"
                    value={data.title}
                    variant="standard"
                    type="text"
                    size="small"
                    fullWidth
                />
            </CardContent>
            <Grid container>
                <Grid item xs={6} md={7}>
                    <Card sx={{ margin: 1 }}>
                        <Stack spacing={2} sx={{ padding: 1 }}>
                            <TextField
                                id="repetitions"
                                label="Repetitions"
                                variant="filled"
                                type="number"
                                size="small"
                                onChange={updateExercise}
                            />
                            <TextField
                                id="sets"
                                label="Sets"
                                variant="filled"
                                type="number"
                                size="small"
                                onChange={updateExercise}
                            />
                        </Stack>
                    </Card>
                </Grid>
                <Grid item xs={6} md={5}>
                    <Card sx={{ margin: 1 }}>
                        <Stack spacing={2} sx={{ padding: 2 }}>
                            <Button variant="outlined" color="error" startIcon={<DeleteIcon />}>
                                remove
                            </Button>

                        </Stack>
                    </Card>
                </Grid>


            </Grid>
        </Card>
    )
}