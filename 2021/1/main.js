$(document).ready(()=>{
    console.log(inputData);
    let decreaseCount = 0;
    inputData.forEach((val,key) => {
        if(inputData[key-1] && inputData[key-1] < val) {
            decreaseCount++;
        }
    });
    console.log(decreaseCount);


    decreaseCount = 0;
    for(let key=4; key <= inputData.length; key++) {
        let totalOne = inputData.slice(key-4,key-1).reduce((prev,current) => prev+current);
        let totalTwo = inputData.slice(key-3,key).reduce((prev,current) => prev+current);
        
        if(totalOne < totalTwo) {
            decreaseCount++;
        }
    }
    console.log(decreaseCount);
    // let decreaseCount = 0;
    // inputData.forEach((val,key) => {
    //     if(inputData[key-3]) {
    //         console.log(inputData.slice(key-3,key-1));
    //         console.log(inputData.slice(key-2,key));
    //     }
    // });
    

});