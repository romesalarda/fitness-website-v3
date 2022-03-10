import React from 'react'

import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import FormControl from '@mui/material/FormControl'
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import { Box, Stack } from '@mui/material'
import Checkbox from '@mui/material/Checkbox';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';

// create new set
export default function ExerciseInput({ handleCreate, handleChangeInput, value }) {
    return (
        <Paper
            component="form"
            sx={{ p: '10px 4px', display: 'flex', alignItems: 'center', margin: 2 }}
            onSubmit={handleCreate}
        >
            <FormControl>

                <Stack direction="row">
                    <TextField
                        placeholder="Create new exercise"
                        sx={{ margin: 1 }}
                        inputProps={{ 'aria-label': 'create new set' }}
                        fullWidth
                        size='small'
                        required
                        value={value}
                        onChange={handleChangeInput}
                        variant="standard"
                    />
                    <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                        <AddIcon />
                    </IconButton>
                </Stack>

                <Stack direction="row">
                    <TextField
                        placeholder="Repetitions"
                        type="number"
                        inputProps={{ 'aria-label': 'repetitions' }}
                        sx={{ margin: 1 }}
                        fullWidth
                        size='small'
                        required
                        defaultValue={12}
                        variant="outlined"
                        InputProps={{ inputProps: { min: 1 } }}
                        label="repetitions"
                    />
                    <TextField
                        placeholder="Sets"
                        inputProps={{ 'aria-label': 'sets' }}
                        sx={{ margin: 1 }}
                        fullWidth
                        size='small'
                        required
                        type="number"
                        InputProps={{ inputProps: { min: 0 } }}
                        defaultValue={4}
                        variant="outlined"
                        label="sets"
                    />
                    <TextField
                        placeholder="Weight"
                        inputProps={{ 'aria-label': 'Weight' }}
                        sx={{ margin: 1 }}
                        fullWidth
                        size='small'
                        required
                        type="number"
                        InputProps={{ inputProps: { min: 0 } }}
                        defaultValue={4}
                        variant="outlined"
                        label="weight"
                    />
                    <Checkbox
                        id="public"

                        checked={true}
                        icon={<PublicOffIcon />}
                        checkedIcon={<PublicIcon />}
                    />
                </Stack>

            </FormControl>

            <FormGroup sx={{ ml: 1, flex: 1 }}>
                <IconButton >
                    <SwapHorizIcon />
                </IconButton>
            </FormGroup>
        </Paper >
    )
}
