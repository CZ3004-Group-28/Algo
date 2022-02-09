import React, {forwardRef, useEffect, useImperativeHandle, useRef, useState} from "react";
import {Typography} from "@mui/material";

type Props = {
	callback: () => void;
}

const Timer = forwardRef((props: Props, ref) => {
	const [value, setValue] = useState<number>(100);
	const timeRef = useRef<any>();
	const valueHolder = useRef<number>(30);

	useEffect(() => {
		return () => {
			clearTimeout(timeRef.current)
		}
	}, []);

	useImperativeHandle(ref, () => ({
		reset(){
			valueHolder.current = 30;
			update();
		}
	}));

	const update = () => {
		if (valueHolder.current < 0) return;

		if (valueHolder.current === 0) {
			alert("Time out, robot stops");
			props.callback();
		}

		setValue(valueHolder.current);
		valueHolder.current -= 1;
		timeRef.current = setTimeout(update, 1000);
	};

	return <Typography variant="h1" component="h2" style={{fontSize: 16, color: 'red', textAlign: 'center'}}>
		Time left: {value} s
	</Typography>
})

export default Timer;
