window.onload = function () {
  var app = new Vue({
    el: '#app',
    delimiters: ['${', '}$'],
    data: {
      status: "",
      seen: false,
      viewData: false,
      originalData: "",
      grades: "",
      viewCalc: false,
      viewLogin: true,
      categories: {},
      finalGrade: 0.0,
      currentClass: {}
    },
    methods: {
      retrieve: function (event) {
        this.seen = true
        this.status = ""
        setTimeout(function(){countdown();}, 800)

        axios.post('./api/retrieve', {
          username: this.$refs.username.value,
          password: this.$refs.password.value
        })
        .then(response => {
          if(response.headers["content-type"].includes("json")){
            this.grades = response.data
            this.originalData = response.data;
            this.viewLogin = false;
            this.viewData = true;
          }else{
            this.seen = false
            this.status = response.data
          }
        })
      },

      save_data: function(event){
        download(JSON.stringify(this.originalData), "SynergyGradeCalc_SavedData.json", "application/json")
      },

      load_data: function(event){
        var content;
        var file = document.getElementById("load_file").files.item(0);
        var reader = new FileReader();

        reader.onload = function() {
          content =  JSON.parse(reader.result);
          this.originalData = JSON.parse(reader.result);
        }.bind(this)

        reader.readAsText(file);

        setTimeout(function(){
          this.grades = content;
          this.viewLogin = false;
          this.viewData = true;
        }.bind(this), 1000)
      },

      viewGrades: function(value, first){
        if(first == false){
          var aTable = document.getElementById("assignments");
          while (aTable.rows.length > 1) {
            aTable.deleteRow(1);
          }
        }

        this.viewData = false;
        this.viewCalc = true;
        this.currentClass = value;

        for(let i in value[2]){
          setTimeout(function(){
            document.getElementById("className").innerHTML = value[0].split(": ")[1];

            let table = document.getElementById("assignments");
            let thead = table.createTHead();
            let row = thead.insertRow();
            row.classList.add("table-default");
            for (let key of value[2][i]) {
              let th = document.createElement("th");
              let text = document.createTextNode(key);
              th.appendChild(text);
              row.appendChild(th);
            }
          }.bind(this), 1000)
        }

        this.calcGrade(value)
      },

      addAssignment: function(){
        var name = document.getElementById("assignName").value;
        var grade1 = document.getElementById("grade1").value;
        var grade2 = document.getElementById("grade2").value;
        var type = document.getElementById("categor").value;

        if(name != "" && grade1 != "" && grade2 != "" && type != ""){
          if(this.categories.hasOwnProperty(type)){
            var grade = (grade1 + "/" + grade2);
            var temp = this.currentClass;
            temp[2].unshift([name, grade, type]);
            this.viewGrades(temp, false);
          }else{
            document.getElementById("calcStatus").innerHTML = "Category does not exist"
          }
        }else{
          document.getElementById("calcStatus").innerHTML = "Inputs cannot be blank"
        }
      },

      removeAssignment: function(){
        var temp = this.currentClass;
        temp[2].shift();
        this.viewGrades(temp, false);
      },

      calcGrade: function(value){
        for(let p of value[1]){
          this.categories[p[0]] = parseFloat(p[1]);
        }

        var cateGrades = new Array(value[1].length)
        for(var l = 0; l < cateGrades.length; l++){
          cateGrades[l] = new Array(0, 0);
        }
        var cateList = []

        for(let i of value[1]){
          cateList.push(i[0]);
        }

        for(let i in value[2]){
          cateGrades[cateList.indexOf(value[2][i][2])][0] += parseFloat(value[2][i][1].split("/")[0]);
          cateGrades[cateList.indexOf(value[2][i][2])][1] += parseFloat(value[2][i][1].split("/")[1]);
        }

        var total = 0.0;
        var totalC = 0.0;
        for(let o in cateGrades){
          if(cateGrades[o][1] != 0){
            total += (cateGrades[o][0]/cateGrades[o][1])*this.categories[cateList[o]];
            totalC += this.categories[cateList[o]];
          }
        }

        this.finalGrade = Math.floor((total/totalC) * 10000) / 100;
      },

      dataPanel: function(){
        this.viewCalc = false;
        this.viewLogin = false;
        this.grades = this.originalData;
        this.viewData = true;
      }
    },

  })
}

var seconds;
var temp;

function countdown() {
  seconds = document.getElementById('countdown').innerHTML;
  seconds = parseInt(seconds);

  if (seconds == 1) {
    temp = document.getElementById('countdown');
    temp.innerHTML = "Finished";
    return;
  }

  seconds--;
  temp = document.getElementById('countdown');
  temp.innerHTML = seconds;
  timeoutMyOswego = setTimeout(countdown, 1000);
}

function download(contentD, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([contentD], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}
