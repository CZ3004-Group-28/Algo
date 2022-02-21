import React, {ChangeEvent, useEffect, useState} from "react";
import {
	Button,
	Container,
	Grid,
	IconButton,
	Table,
	TableBody,
	TableCell,
	TableRow,
	TextField, Tooltip,
	Typography
} from "@mui/material";
import {ChevronLeft, ChevronRight} from "@mui/icons-material";
import QueryAPI from "./QueryAPI";

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

type CellState = { x: number, y: number};
type RobotCell = { x: number, y: number, d: Direction | null};

const transformCoord = (x: number, y: number) => {
	return {x: 19 - y, y: x}
}

function FastestCar() {
	const [robotState, setRobotState] = useState<RobotCell>({x: 1, y: 1, d: Direction.NORTH});
	const [obstacles, setObstacles] = useState<CellState[]>([]);
	const [robotX, setRobotX] = useState<number | undefined>(undefined);
	const [robotY, setRobotY] = useState<number | undefined>(undefined);

	const [goalX, setGoalX] = useState<number | undefined>(undefined);
	const [goalY, setGoalY] = useState<number | undefined>(undefined);

	const [page, setPage] = useState<number>(0);
	const [path, setPath] = useState<RobotCell[]>([]);
	const [isComputing, setIsComputing] = useState<boolean>(false);
	const generateRobotCells = () => {
		const robotCells: RobotCell[] = [];
		let markerX = 0;
		let markerY = 0;

		if (robotState.d === Direction.NORTH) {
			markerY++;
		} else if (robotState.d === Direction.EAST) {
			markerX++;
		} else if (robotState.d === Direction.SOUTH) {
			markerY--;
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
						d: robotState.d
					})
				} else {
					robotCells.push({
						x: coord.x,
						y: coord.y,
						d: null
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
					cells.push(
						<TableCell style={{...baseStyle, backgroundColor: 'blue'}}/>
					)
				} else if (foundRobotCell) {
					if (foundRobotCell.d !== null) {
						cells.push(
							<TableCell style={{...baseStyle, backgroundColor: 'yellow'}}/>
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

	const onChangeRobotX = (event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
		if (Number.isInteger(Number(event.target.value))) {
			const nb = Number(event.target.value);
			if (0 < nb && nb < 20) {
				setRobotX(nb);
				return;
			}
		}

		setRobotX(0);
	}

	const onChangeRobotY = (event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
		if (Number.isInteger(Number(event.target.value))) {
			const nb = Number(event.target.value);
			if (0 < nb && nb < 14) {
				setRobotY(nb);
				return;
			}
		}

		setRobotY(0);
	}

	const onChangeGoalX = (event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
		if (Number.isInteger(Number(event.target.value))) {
			const nb = Number(event.target.value);
			if (0 < nb && nb < 14) {
				setGoalX(nb);
				return;
			}
		}

		setGoalX(0);
	}

	const onChangeGoalY = (event: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
		if (Number.isInteger(Number(event.target.value))) {
			const nb = Number(event.target.value);
			if (0 < nb && nb < 19) {
				setGoalY(nb);
				return;
			}
		}

		setGoalY(0);
	}

	const onSetPosition = () => {
		if (!robotX || !robotY || !goalX || !goalY) return;
		setRobotState({x: robotX, y: robotY, d: Direction.NORTH});

		const obs = [];
		for (let i = 0; i < 6; i++) {
			obs.push({x: goalX + i, y: goalY})
		}

		for (let i = -3; i < 5; i++) {
			obs.push({x: robotX + i, y: robotY - 2})
		}

		for (let i = -1; i < 4; i++) {
			obs.push({x: robotX - 3, y: robotY + i});
			obs.push({x: robotX + 4, y: robotY + i});
		}

		setObstacles(obs);
	}

	const compute = () => {
		if (!robotX || !robotY || !goalX || !goalY) return;
		setIsComputing(true);
		QueryAPI.fastest(robotX, robotY, goalX, goalY, (data: any, err: any) => {
			if (data) {
				setPath(data.data.path as RobotCell[]);
			}

			setIsComputing(false);
		})
	};

	useEffect(() => {
		if (page >= path.length) return;
		setRobotState(path[page])
	}, [page])

	return (
		<Container maxWidth="sm" style={{marginTop: 20}}>
			<Grid container spacing={1} justifyContent="center" alignItems="center">
				<Grid item xs={4}>
					<TextField
						onChange={onChangeRobotX}
						value={robotX}
						type="number"
						id="outlined-basic"
						label="Robot X"
						size='small'
						variant="outlined"/>
				</Grid>
				<Grid item xs={4}>
					<TextField
						onChange={onChangeRobotY}
						value={robotY}
						type="number"
						id="outlined-basic"
						label="Robot Y"
						size='small'
						variant="outlined"/>
				</Grid>
			</Grid>

			<Grid container spacing={1} justifyContent="center" alignItems="center">
				<Grid item xs={4}>
					<TextField
						onChange={onChangeGoalX}
						value={goalX}
						type="number"
						id="outlined-basic"
						label="Goal X"
						size='small'
						variant="outlined"/>
				</Grid>
				<Grid item xs={4}>
					<TextField
						onChange={onChangeGoalY}
						value={goalY}
						type="number"
						id="outlined-basic"
						label="Goal Y"
						size='small'
						variant="outlined"/>
				</Grid>
			</Grid>

			<Grid container direction='row' width={200} spacing={1} style={{marginLeft: 'auto', marginRight: 'auto'}}>
				<Grid item xs={6} justifyContent='center'>
					<Button variant='outlined' onClick={onSetPosition} size="small">Set Position</Button>
				</Grid>
				{/*<Grid item xs={4} justifyContent='center'>*/}
				{/*	<Button variant='outlined' onClick={onReset} size="small" disabled={isComputing}>Reset</Button>*/}
				{/*</Grid>*/}
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
				<IconButton disabled={page === path.length - 1} onClick={() => {
					setPage(page + 1)
				}}>
					<ChevronRight/>
				</IconButton>
			</div>}

			<Table style={{width: 'fit-content', marginTop: 20}} aria-label="simple table">
				<TableBody>
					{renderGrid()}
				</TableBody>
			</Table>
		</Container>
	)
}

export default FastestCar;
