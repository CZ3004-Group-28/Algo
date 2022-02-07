import React, {ChangeEvent, useEffect, useState} from 'react';
import './App.css';
import {
	Button,
	Chip,
	Container,
	Grid,
	IconButton,
	MenuItem,
	Select,
	Table,
	TableBody,
	TableCell,
	TableRow,
	TextField, Tooltip,
	Typography
} from '@mui/material';
import QueryAPI from "./QueryAPI";
import {ChevronLeft, ChevronRight} from "@mui/icons-material";

enum Direction {
	NORTH = 0,
	NORTH_EAST = 1,
	EAST = 2,
	EAST_SOUTH = 3,
	SOUTH = 4,
	SOUTH_WEST = 5,
	WEST = 6,
	WEST_NORTH = 7,
}

enum ObDirection {
	NORTH = 0,
	EAST = 2,
	SOUTH = 4,
	WEST = 6,
}

const DirectionToString = {
	0: 'North',
	1: 'North East',
	2: 'East',
	3: 'East South',
	4: 'South',
	5: 'South West',
	6: 'West',
	7: 'West North'
}

type CellState = { x: number, y: number, d: Direction, id: number};
//
// const obstacles: CellState[] = [
// 	{x: 10, y: 15, d: Direction.EAST},
// 	{x: 12, y: 5, d: Direction.NORTH},
// 	{x: 18, y: 17, d: Direction.SOUTH},
// 	{x: 5, y: 9, d: Direction.WEST}
// ]

type RobotCell = { x: number, y: number, d: Direction | null, s: number };

const transformCoord = (x: number, y: number) => {
	return {x: 19 - y, y: x}
}

function App() {
	const [robotState, setRobotState] = useState<RobotCell>({x: 1, y: 1, d: Direction.NORTH, s: -1});
	const [obstacles, setObstacles] = useState<CellState[]>([]);
	const [obXInput, setObXInput] = useState<number | undefined>(undefined);
	const [obYInput, setObYInput] = useState<number | undefined>(undefined);
	const [directionInput, setDirectionInput] = useState<ObDirection>(ObDirection.NORTH);
	const [isComputing, setIsComputing] = useState<boolean>(false);
	const [path, setPath] = useState<RobotCell[]>([]);
	const [commands, setCommands] = useState<string[]>([]);
	const [page, setPage] = useState<number>(0);

    const generateNewID = () => {
        while (true){
            let new_id = Math.floor(Math.random() * 10) + 1;  // just try to generate an id;
            let ok = true;
            for (const ob of obstacles){
                if (ob.id === new_id){
                    ok=false;
                    break;
                }
            }
            if (ok){
                return new_id;
            }
        }
        return -1;
    }

	const generateRobotCells = () => {
		const robotCells: RobotCell[] = [];
		let markerX = 0;
		let markerY = 0;

		if (robotState.d === Direction.NORTH) {
			markerY++;
		} else if (robotState.d === Direction.NORTH_EAST) {
			markerY++;
			markerX++;
		} else if (robotState.d === Direction.EAST) {
			markerX++;
		} else if (robotState.d === Direction.EAST_SOUTH) {
			markerX++;
			markerY--;
		} else if (robotState.d === Direction.SOUTH) {
			markerY--;
		} else if (robotState.d === Direction.SOUTH_WEST) {
			markerY--;
			markerX--;
		} else if (robotState.d === Direction.WEST) {
			markerX--;
		} else {
			markerX--;
			markerY++;
		}

		for (let i = -1; i < 2; i++) {
			for (let j = -1; j < 2; j++) {
				const coord = transformCoord(robotState.x + i, robotState.y + j);
				if (markerX === i && markerY === j) {
					robotCells.push({
						x: coord.x,
						y: coord.y,
						d: robotState.d,
						s: robotState.s
					})
				} else {
					robotCells.push({
						x: coord.x,
						y: coord.y,
						d: null,
						s: -1
					})
				}
			}
		}

		return robotCells;
	};

	const renderGrid = (): React.ReactNode[] => {
		const rows = [];
		const baseStyle = {
			width: 25,
			height: 25,
			borderStyle: 'solid',
			borderTopWidth: 1,
			borderBottomWidth: 1,
			borderLeftWidth: 1,
			borderRightWidth: 1,
			padding: 0
		};

		const robotCells = generateRobotCells();
		for (let i = 0; i < 20; i++) {
			const cells = [<TableCell style={{padding: 0, width: 25, height: 25}}><Typography
				fontSize={12}>{19 - i}</Typography></TableCell>];
			for (let j = 0; j < 20; j++) {
				let foundOb: CellState | null = null;
				let foundRobotCell: RobotCell | null = null;

				for (const ob of obstacles) {
					const transformed = transformCoord(ob.x, ob.y)
					if (transformed.x === i && transformed.y === j) {
						foundOb = ob;
						break;
					}
				}

				if (!foundOb) {
					for (const cell of robotCells) {
						if (cell.x === i && cell.y === j) {
							foundRobotCell = cell;
							break
						}
					}
				}

				if (foundOb) {
					if (foundOb.d === Direction.WEST) {
						cells.push(
							<TableCell style={{
								...baseStyle,
								borderLeftWidth: 4,
								borderLeftColor: 'red',
								width: 21,
								backgroundColor: 'blue'
							}}/>
						)
					} else if (foundOb.d === Direction.EAST) {
						cells.push(
							<TableCell style={{
								...baseStyle,
								borderRightWidth: 4,
								borderRightColor: 'red',
								width: 21,
								backgroundColor: 'blue'
							}}/>
						)
					} else if (foundOb.d === Direction.NORTH) {
						cells.push(
							<TableCell style={{
								...baseStyle,
								borderTopWidth: 4,
								borderTopColor: 'red',
								width: 21,
								backgroundColor: 'blue'
							}}/>
						)
					} else if (foundOb.d === Direction.SOUTH) {
						cells.push(
							<TableCell style={{
								...baseStyle,
								borderBottomWidth: 4,
								borderBottomColor: 'red',
								width: 21,
								backgroundColor: 'blue'
							}}/>
						)
					}
				} else if (foundRobotCell) {
					if (foundRobotCell.d !== null) {
						cells.push(
							<TableCell style={{...baseStyle, backgroundColor: foundRobotCell.s != -1 ? 'red' : 'yellow'}}/>
						)
					} else {
						cells.push(
							<TableCell style={{...baseStyle, backgroundColor: 'green'}}/>
						)
					}
				} else {
					cells.push(
						<TableCell style={{...baseStyle, borderColor: 'black'}}/>
					)
				}
			}

			rows.push(
				<TableRow>
					{cells}
				</TableRow>
			)
		}

		const yAxis = [<TableCell style={{padding: 0, width: 25, height: 25}}/>];
		for (let i = 0; i < 20; i++) {
			yAxis.push(
				<TableCell style={{padding: 0, width: 25, height: 25}}>
					<Typography style={{width: '100%', textAlign: 'center'}}
								fontSize={12}>{i}</Typography>
				</TableCell>
			)
		}
		rows.push(
			<TableRow>
				{yAxis}
			</TableRow>
		)
		return rows;
	};

	const onChangeX = (event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
		if (Number.isInteger(Number(event.target.value))) {
			const nb = Number(event.target.value);
			if (0 < nb && nb < 20) {
				setObXInput(nb);
				return;
			}
		}

		setObXInput(0);
	}

	const onChangeY = (event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
		if (Number.isInteger(Number(event.target.value))) {
			const nb = Number(event.target.value);
			if (0 < nb && nb < 19) {
				setObYInput(nb);
				return;
			}
		}

		setObYInput(0);
	}

	const onClick = () => {
		if (!obXInput || !obYInput) return;
		const newObstacles = [...obstacles];

		newObstacles.push({
			x: obXInput,
			y: obYInput,
			d: directionInput as unknown as Direction,
			id: generateNewID()
		})

		setObstacles(newObstacles);
	};

	const onDirectionInputChange = (event: any) => {
		// @ts-ignore
		setDirectionInput(event.target.value as Direction)
	}

	const onRemoveObstacle = (ob: CellState) => {
		if (path.length > 0 || isComputing) return;
		const newObstacles = [];

		for (const o of obstacles) {
			if (o.x === ob.x && o.y === ob.y) continue;
			newObstacles.push(o);
		}

		setObstacles(newObstacles);
	};

	const compute = () => {
		setIsComputing(true);
		QueryAPI.query(obstacles, (data: any, err: any) => {
			if (data) {
				setPath(data.data.path as RobotCell[]);
				setCommands(data.data.commands);
			}

			setIsComputing(false);
		})
	};

	const onReset = () => {
		setRobotState({x: 1, y: 1, d: Direction.NORTH, s: -1});
		setPath([]);
		setCommands([]);
		setPage(0);
	}

	useEffect(() => {
		if (page >= path.length) return;
		setRobotState(path[page])
	}, [page])

	return (
		<Container maxWidth="sm">
			<Typography style={{textAlign: 'center', margin: 10}}>Robot motion simulator</Typography>
			<Grid container spacing={1} justifyContent="center" alignItems="center">
				<Grid item xs={3}>
					<TextField
						onChange={onChangeX}
						value={obXInput}
						type="number"
						id="outlined-basic"
						label="Obstacle X"
						size='small'
						variant="outlined"/>
				</Grid>
				<Grid item xs={3}>
					<TextField
						onChange={onChangeY}
						value={obYInput}
						type="number"
						id="outlined-basic"
						label="Obstacle Y"
						size='small'
						variant="outlined"/>
				</Grid>
				<Grid item xs={3}>
					<Select
						labelId="demo-simple-select-label"
						id="demo-simple-select"
						value={directionInput}
						label="Direction"
						size="small"
						onChange={onDirectionInputChange}
					>
						<MenuItem value={ObDirection.NORTH}>North</MenuItem>
						<MenuItem value={ObDirection.SOUTH}>South</MenuItem>
						<MenuItem value={ObDirection.EAST}>East</MenuItem>
						<MenuItem value={ObDirection.WEST}>West</MenuItem>
					</Select>
				</Grid>
				<Grid item xs={3}>
					<Button onClick={onClick} disabled={!obXInput || !obYInput || isComputing || path.length > 0}
							variant="outlined" size='small'>Add Obstacle</Button>
				</Grid>
			</Grid>

			<Grid container spacing={1} style={{marginTop: 10, marginBottom: 10}}>
				{obstacles.map((ob) => {
					return (
						<Grid item>
							<Chip label={`x: ${ob.x}  y: ${ob.y}  d: ${DirectionToString[ob.d]}`}
								  onDelete={() => onRemoveObstacle(ob)}/>
						</Grid>
					)
				})}
			</Grid>
			<Grid container direction='row' width={200} spacing={1} style={{marginLeft: 'auto', marginRight: 'auto'}}>
				<Grid item xs={6} justifyContent='center'>
					<Button variant='outlined' onClick={onReset} size="small" disabled={isComputing}>Reset</Button>
				</Grid>
				<Grid item xs={6}>
					<Button variant='contained' size="small" disabled={obstacles.length === 0 || isComputing}
							onClick={compute}>Compute</Button>
				</Grid>
			</Grid>

			{path.length > 0 && <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'center'}}>
				<IconButton disabled={page === 0} onClick={() => {
					setPage(page - 1)
				}}>
					<ChevronLeft/>
				</IconButton>
				<Typography
					style={{paddingTop: 8, marginLeft: 5, marginRight: 5}}>Step: {page + 1} / {path.length}</Typography>
				<Tooltip title={page < commands.length ? commands[page] : ""}>
					<IconButton disabled={page === path.length - 1} onClick={() => {
						setPage(page + 1)
					}}>
						<ChevronRight/>
					</IconButton>
				</Tooltip>
			</div>}

			<Table style={{width: 'fit-content', marginTop: 20}} aria-label="simple table">
				<TableBody>
					{renderGrid()}
				</TableBody>
			</Table>
		</Container>
	);
}

export default App;
