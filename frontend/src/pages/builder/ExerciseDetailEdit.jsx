import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { Divider } from '@mui/material';
import { MenuItem, Select, InputLabel, FormControl, IconButton, Stack } from '@mui/material';

export default function ExerciseEditDetail({ data, handleClose, open, updateSelectFields, updateTextFields, updateCheckedFields }) {

    return (
        <div>
            <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth={true}>
                <DialogTitle>Editing '{data.title}'</DialogTitle>
                <DialogContent>
                    <DialogContentText style={{ marginBottom: "2vh" }}>
                        Created: {new Date(data.created).toUTCString()}
                    </DialogContentText>
                    <Stack spacing={2}>
                        <TextField

                            id="description"
                            label="description"
                            type="text"
                            fullWidth
                            variant="standard"
                            value={data.description}
                            onChange={updateTextFields}
                            multiline
                            maxRows={5}
                        />
                    </Stack>
                    <Stack direction="row" spacing={2} sx={{ margin: 1, padding: 2 }}>
                        <FormControl style={{ minWidth: 150 }}>
                            <InputLabel id="level-lable">Level</InputLabel>
                            <Select
                                labelId="level-lable"
                                id="level"
                                value={data.level}
                                label="level"
                                name="level"
                                onChange={updateSelectFields}
                            >
                                <MenuItem value={"1"}>Beginner</MenuItem>
                                <MenuItem value={"2"}>Intermediate</MenuItem>
                                <MenuItem value={"3"}>Advanced</MenuItem>

                            </Select>
                        </FormControl>
                        <FormControl style={{ minWidth: 150 }}>
                            <InputLabel id="target-lable">Target</InputLabel>
                            <Select
                                labelId="target-lable"
                                id="target"
                                value={data.target}
                                label="target"
                                name="target"
                                onChange={updateSelectFields}
                            >
                                <MenuItem value={"1"}>Lower</MenuItem>
                                <MenuItem value={"2"}>Upper</MenuItem>
                                <MenuItem value={"3"}>Core</MenuItem>

                            </Select>
                        </FormControl>
                        <FormControl style={{ minWidth: 150 }}>
                            <InputLabel id="direction-lable">Direction</InputLabel>
                            <Select
                                labelId="direction-lable"
                                id="direction"
                                value={data.direction}
                                label="direction"
                                name="direction"
                                onChange={updateSelectFields}
                            >
                                <MenuItem value={"1"}>Horizontal</MenuItem>
                                <MenuItem value={"2"}>Vertical</MenuItem>
                            </Select>
                        </FormControl>
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Ok</Button>
                </DialogActions>
            </Dialog>
        </div >
    );
}