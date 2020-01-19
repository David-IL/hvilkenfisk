var getArtsData = function() {
    var artsData;
    try {
        fetch('Arter.json')
            .then(function(resp) {
                return resp.json();
            })
            .then(function(data) {
                artsData = data;
            });        
    } catch (err) {
        console.log(err);
    };
    return artsData;
};

// fetch data on species from 'Arter.json' and save in object artsData
var artsData;
try {
    fetch('Arter.json')
        .then(function(resp) {
            return resp.json();
        })
        .then(function(data) {
            artsData = data;
        });
} catch (err) {
    console.log(err);
}

function readImg(input) {
    var fileEl;
    if (input.files && input.files[0]) {
        fileEl = input.files[0];
    } else if (input && input[0]) {
        fileEl = input[0];
    } else {
        return;
    }
    var reader = new FileReader();

    reader.onload = function (e) {
        // Remove text inside drop image area   
        try {
            var element = document.getElementById("my-form");
            element.parentNode.removeChild(element);
        } catch (err) {
            console.log(err);
        }

        $('#your_img').attr('src', e.target.result);                     
    };

    reader.readAsDataURL(fileEl);   
    console.log(fileEl) ;
}

// FISH CONTROLLER
var fishController = (function() {    
    
    return {               
        testing: function() {
            console.log(data);
        }
    };
    
})();


// UI CONTROLLER
var UIController = (function() {
    
    var DOMstrings = {
        topPart: '.top',
        choosePictureButton: '.button_choose_picture', 
        dropImageArea: '#drop-area',       
        imgToUpload: '.fileElem',
        inputWaterType: '.add_water_type',
        inputLength: '.add__length',
        inputWeight: '.add__weight', 
        checkSpeciesBtn: '.btn_check_species',                       
        predictionContainer: '.fish__suggestion__list',        
        container: '.container_predictions',        
        dateLabel: '.page__date--date'
    };   
    

    var formatPercentage = function(num) {
        /*
        Turn probability to percentage, e.g. 0.7654 -> 76% 
        */
        num = Math.abs(num * 100)

        return num
    }

    var convert_fish_names = function(fishname) {
        /*
        Convert Norwegian characters in fishname to non-norwegian,
        i.e. 'æ' -> 'ae', 'ø' -> 'o', 'å' -> 'aa'.
    
        Also replace space and . with underbar, i.e. ' ' -> '_', '.' -> '_'
        */
       fishname = fishname.replace(/æ/gi, 'ae').replace(/Æ/gi, 'Ae');
       fishname = fishname.replace(/ø/gi, 'o').replace(/Ø/gi, 'O');
       fishname = fishname.replace(/å/gi, 'aa').replace(/Å/gi, 'Aa');
       fishname = fishname.replace(/ /gi, '_') .replace('.', '_');
    
       return fishname;
    }

    var formatWeight = function(num, fixed_decimal_places=2, missing_text='Ukjent') {
        /* 
        If weight in [g] is above 1000, then rewrite as [kg]
        */
        num = parseFloat(num);        
       
        if ((num == '') || (num == null) || isNaN(num)) {
            return(`<i>${missing_text}</i>`)
        } else if (num > 100000.0){
            num = Math.round(num / 1000);
            return `${num} kg`
        } else if (num > 10000.0){
            num = parseFloat(Math.round(num) / 1000).toFixed(1);
            return `${num} kg`
        } else if (num > 1000.0) {
            num = parseFloat(Math.round(num) / 1000).toFixed(fixed_decimal_places);
            return `${num} kg`
        } else {
            return `${num} g`
        }
    };    

    var check_if_link_is_valid = function(link_str) {        
        if ((link_str == '') || (link_str == null)) {
            return false;
        } else {
            return true;
        };
    };

    var prediction_table = function(fish_obj, probability, pred_number_text) {
        //console.log(`${fish_obj.Art}: ${probability}`);

        // Add url to species
        var latin_name = fish_obj.Latin;

        if (check_if_link_is_valid(fish_obj.Link)) {
            latin_name = `<a href=${fish_obj.Link} target="_blank">${latin_name}</a>`;        
        };
        
        // Add url to record fish
        var record = formatWeight(fish_obj.Norgesrekord, fixed_decimal_places=2,
            missing_text='Ikke tatt på stang');
        
        if (check_if_link_is_valid(fish_obj.Link_rekord)) {
            record = `<a href=${fish_obj.Link_rekord} target="_blank">${record}</a>`;
        } else {
            record = `${record}`;
        };

        // make list of similar species (in html)
        var similar_species = '';
        /*
        if (fish_obj.Maximum_dyp.length > 0) {
            for (var i = 0; i < fish_obj.Maximum_dyp.length; i++) {
                similar_species += fish_obj.similar_species[i] + '<br>';
            }
            row_length_similar_spec = fish_obj.Maximum_dyp.length;
        } else {
            similar_species += '<i>ingen</i>';
            row_length_similar_spec = 1;
        }
        */                     
        
        // display reference fish image if available
        var img_src = `ref_fish_imgs/${convert_fish_names(fish_obj.Art)}.jpg`;
        //console.log(img_src);

        var html_text = `
            <div id="${pred_number_text}_prediction" class="pred_box">                                                      
                <div class="pred_text">                                                   
                    <div class="predicted_fish_title">${fish_obj.Art}</div>
                    <div class="predicted_fish_prob" id="pred_prob_${pred_number_text}">
                        ${formatPercentage(probability)}% sannsynlighet
                    </div>
                    <div class="pred_table clearfix">
                        <table>  
                            <tr>
                                <td>Familie</td>
                                <td>${fish_obj.Familie}</td> 
                            </tr>                                                
                            <tr>
                                <td>Latinsk navn</td>
                                <td><i>${latin_name}</i></td> 
                            </tr>
                            <tr>
                                <td>Lengde</td>
                                <td>Opptil ${fish_obj.Lengde}cm</td> 
                            </tr>
                            <tr>
                                <td>Vekt</td>
                                <td>Opptil ${formatWeight(fish_obj.Vekt)}</td> 
                            </tr>
                            <tr>
                                <td>Norgesrekord</td>
                                <td>${record}</td> 
                            </tr>
                            <tr>
                                <!--<td>Kan forveksles med</td>-->
                                <td>Lignende arter</td>
                                <td>${similar_species}</td> 
                            </tr>
                        </table>
                    </div>            
                </div>          
                <div class="fish_image_ref" id="img_ref_${pred_number_text}">                    
                    <img id="pred_img_${pred_number_text}" src="${img_src}" onclick="window.open('${img_src}', '_blank');">                     
                </div>                 
                
            </div>`;
        return html_text;
    }

    var handleFile = function(files) {  
        //console.log(files);
        //([...files]).forEach(readImg);         
        readImg(files);
    };

    var uploadFile = function(file) {
        let url = '127.0.0.1:1337/uploaded_imgs/'
        let formData = new FormData()
        console.log(`Trying to upload to ${url}`);

        formData.append('file', file)

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(() => { 
            console.log("File was uploaded succesfully"); 
        })
        .catch(() => { 
            console.log("File was not uploaded, an error occurred");
        })
    };

    return {
        getInput: function() {
            return {
                waterType: document.querySelector(DOMstrings.inputWaterType).value, // Will be either inc or exp
                length: parseFloat(document.querySelector(DOMstrings.inputLength).value),
                weight: parseFloat(document.querySelector(DOMstrings.inputWeight).value)
            };
        },        
        
        clearFields: function() {
            var fields, fieldsArr;
            
            fields = document.querySelectorAll(DOMstrings.inputDescription + ', ' + DOMstrings.inputValue);
            
            fieldsArr = Array.prototype.slice.call(fields);
            
            fieldsArr.forEach(function(current, index, array) {
                current.value = "";
            });
            
            fieldsArr[0].focus();
        },

        clearPrediction: function() {
            document.querySelector(DOMstrings.container).innerHTML = '';
        },
        
        
        displayPredictions: function(fish_predictions, probs) {             
            var newHtml1, newHtml2, newHtml3;
            
            newHtml1 = prediction_table(fish_predictions[0], probs[0], 'first');
            newHtml2 = prediction_table(fish_predictions[1], probs[1], 'second');
            newHtml3 = prediction_table(fish_predictions[2], probs[2], 'third');

            // Insert the HTML into the DOM
            document.querySelector(DOMstrings.container).insertAdjacentHTML('beforeend', newHtml1);
            document.querySelector(DOMstrings.container).insertAdjacentHTML('beforeend', newHtml2);
            document.querySelector(DOMstrings.container).insertAdjacentHTML('beforeend', newHtml3);
        },                         
        
        displayDate: function() {
            var now, months, month, year;
            
            now = new Date();
            //var christmas = new Date(2016, 11, 25);
            
            months = ['Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Desember'];
            month = now.getMonth();            
            year = now.getFullYear();
            day = now.getDate();
            document.querySelector(DOMstrings.dateLabel).textContent = '(' + day + '.' + months[month] + ' ' + year + ')';
        },              

        ctrlCallSpeciesAPI: function(inputs) {
            /*
            This function is supposed to call the API where predictions on 
            what fish is computed. For now we only draw random fishes.

            The returned value from the API should be a JSON
            {
                "Ørret:" 0.78,
                "Mort": 0.17,
                "Røye": 0.05
            }
            */
            console.log('Button "Sjekk fisk" pushed');
            console.log(inputs);            
            
            // Draw random species (while API is not yet up)
            function shuffle(o) {
                for(var j, x, i = o.length; i; j = parseInt(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
                return o;
            };

            let species = Object.keys(artsData);
            let temp_arr = shuffle(Array.from(Array(191).keys()));
            let fish_preds = [species[temp_arr[0]], species[temp_arr[1]], species[temp_arr[2]]];
            let pred_probs = [0.68, 0.21, 0.09];

            return [fish_preds, pred_probs];
        },

        ctrlChooseImage: function(files) {
            console.log('Button "Velg bildefil" pushed');
            // ([...files]).forEach(uploadFile);
            handleFile(files);
        },        
        

        // From https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
        preventDefaults: function(e) {
            e.preventDefault();
            e.stopPropagation();
        },

        highlight: function(e) {
            document.querySelector(DOMstrings.dropImageArea).classList.add('highlight')
        },
          
        unhighlight: function(e) {
            document.querySelector(DOMstrings.dropImageArea).classList.remove('highlight')
        },

        handleDrop: function(e) {
            let dt = e.dataTransfer;
            let files = dt.files;        
          
            handleFile(files);            
        },

        getDOMstrings: function() {
            return DOMstrings;
        }
    };
    
})();




// GLOBAL APP CONTROLLER
var controller = (function(UICtrl) {
    
    var setupEventListeners = function() {
        var DOM = UICtrl.getDOMstrings();
        
        document.querySelector(DOM.checkSpeciesBtn).addEventListener('click', updatePredictions);        
        //document.querySelector(DOM.choosePictureButton).addEventListener('click', UICtrl.ctrlChooseImage);         
        //document.querySelector(DOM.choosePictureButton).addEventListener('onchange', UICtrl.ctrlChooseImage);         

        // Event listener for imageDrop box
        //    From https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
        let dropArea = document.querySelector(DOM.dropImageArea);

        ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, UICtrl.preventDefaults, false)
        });

        ;['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, UICtrl.highlight, false)
        });
        
        ;['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, UICtrl.unhighlight, false)
        });

        dropArea.addEventListener('drop', UICtrl.handleDrop, false);

        // For image upload button
        //document.querySelector(DOM.imgToUpload).addEventListener('change', UICtrl.ctrlChooseImage);
    };
    
    var updatePage = function() {
        var img_num = Math.floor(Math.random() * 10) + 1;
        //console.log(img_num);

        // 1. New top background image
        topEl = document.querySelector('.top');
        topEl.style["background-image"] = `linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.75)), url(bck_imgs/back${img_num}.jpg)`;
    };


    var updatePredictions = function() {
        
        // 0. Clear current prediction
        UICtrl.clearPrediction();

        // 1. Get the input variables
        var inputVars = UICtrl.getInput();        
        
        // 2. Send input variables and image to API and fetch json
        var [fish_preds, pred_probs] = UICtrl.ctrlCallSpeciesAPI(inputVars);
        //console.log(fish_preds);
        //console.log(pred_probs);
        
        // 3. Pick top 3 predictions and get data from json                
        let fisk1 = artsData[fish_preds[0]];
        let fisk2 = artsData[fish_preds[1]];
        let fisk3 = artsData[fish_preds[2]];
        let fisk_pred = [fisk1, fisk2, fisk3];        

        // 4. Display predictions
        UICtrl.displayPredictions(fisk_pred, pred_probs);
    }; 

    
    return {
        init: function() {
            console.log('Application has started.');
            UICtrl.displayDate();            
            setupEventListeners();
            updatePage();            
        }
    };
    
})(UIController);


controller.init();