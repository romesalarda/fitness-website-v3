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

export default function CardioEdit({ data, handleSwitch, updateTextFields, updateSelectFields }) {

    return (
        <Card sx={{ minWidth: 275, bgcolor: "lightgrey", margin: 2 }} variant="outlined">
            <CardContent>
                <Grid container>
                    <TextField
                        id="title"
                        value={data.title}
                        variant="standard"
                        type="text"
                        size="small"
                        fullWidth
                        sx={{ margin: 1 }}
                    />
                    <Grid item xs={3} md={6}>
                        <Card sx={{ margin: 1 }}>
                            <Stack>
                                <Stack spacing={2} sx={{ padding: 1 }} direction="row">
                                    <TextField
                                        id="duration"
                                        label="duration"
                                        variant="outlined"
                                        type="number"
                                        size="large"
                                        value={data.duration}
                                        onChange={updateTextFields}
                                        sx={{ flex: 6 }}
                                    />
                                    <FormControl>
                                        <InputLabel id="repetiton-unit-lable">Unit</InputLabel>
                                        <Select
                                            labelId="repetiton-unit-lable"
                                            id="repetitions_unit"
                                            value={data.repetitions_unit}
                                            label="Unit"
                                            name="repetitions_unit"
                                            onChange={updateSelectFields}
                                            sx={{ flex: 2 }}
                                        >
                                            <MenuItem value={"1"}>Reps</MenuItem>
                                            <MenuItem value={"2"}>Until failure</MenuItem>
                                            <MenuItem value={"3"}>Seconds</MenuItem>
                                            <MenuItem value={"4"}>Minutes</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Stack>
                                <TextField
                                    id="sets"
                                    label="sets"
                                    variant="outlined"
                                    type="number"
                                    size="large"
                                    value={data.sets}
                                    onChange={updateTextFields}
                                    sx={{ margin: 1 }}
                                />
                            </Stack>

                        </Card>

                    </Grid>
                    <Grid item xs={3} md={6}>
                        <Card sx={{ margin: 1 }}>
                            <Stack spacing={2} sx={{ padding: 1 }} direction="row">
                                <TextField
                                    id="distance"
                                    label="distance"
                                    variant="outlined"
                                    type="number"
                                    size="large"
                                    value={data.distance}
                                    onChange={updateTextFields}
                                    sx={{ flex: 6 }}
                                />
                                <FormControl >
                                    <InputLabel id="weight-unit-lable">Unit</InputLabel>
                                    <Select
                                        labelId="weight-unit-lable"
                                        id="cardio_unit"
                                        name="cardio_unit"
                                        value={data.cardio_unit}
                                        label="unit"
                                        onChange={updateSelectFields}
                                        sx={{ flex: 2 }}
                                    >
                                        <MenuItem value={"1"}>Meters</MenuItem>
                                        <MenuItem value={"2"}>Kilometers</MenuItem>
                                    </Select>
                                </FormControl>

                            </Stack>
                        </Card>

                    </Grid>
                </Grid>
            </CardContent>
            <Divider></Divider>
            <CardActions disableSpacing sx={{ justifyContent: "right" }}>

                <IconButton>
                    <EditIcon />
                </IconButton>
                <IconButton>
                    <DeleteIcon />
                </IconButton>
                <Checkbox
                    id="public"

                    checked={true}
                    icon={<PublicOffIcon />}
                    checkedIcon={<PublicIcon />}
                />
                <IconButton onClick={() => handleSwitch(true)}>
                    <SwapHorizIcon />
                </IconButton>


            </CardActions>
        </Card>
    )
}