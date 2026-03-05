function validateForm(){

let studentID = document.getElementById("student_id").value

if(studentID.length !== 9){
alert("Student ID must be 9 digits")
return false
}

return true
}