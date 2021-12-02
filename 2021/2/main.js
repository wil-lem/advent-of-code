$(document).ready(()=>{
    let pos = {x:0,y:0};
    const re = /^(.*?) (\d+)$/
    inputData.forEach((val) => {
        const m = re.exec(val);
        if(m[2]) {
            let dim = null;
            let mod = 1;
            switch (m[1]) {
                case 'forward':
                    dim = 'x';
                    break;
                case 'up':
                    mod = -1;
                case 'down':
                    dim = 'y';
                    break;
            }
            if(dim) {
                pos[dim] += m[2] * mod;
            }
        }
    });
    console.log(pos);
    console.log(pos.x*pos.y);

    // PART 2
    pos = {x:0,y:0};
    let aim = 0;
    inputData.forEach((val) => {
        const m = re.exec(val);
        if(m[2]) {
            const change = parseInt(m[2])
            switch (m[1]) {
                case 'forward':
                    pos.x += change;
                    pos.y += aim * change;
                    break;
                case 'up':
                    aim -= change;
                    break;
                case 'down':
                    aim += change;
                    break;
            }
        }
    });

    console.log('part 2',pos);
    console.log(pos.x*pos.y);


});

