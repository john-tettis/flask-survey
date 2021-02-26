

const $addQuestion = $('.add-question');
const $addAnswer = $('.add-answer')
class Survey{
    constructor(title, instructions){
        this.questions=[]
        this.title=title
        this.instructions=instructions
    }

    addQuestion(question,answers, allowText){
        let surveyQuestion ={
            question,
            answers,
            allowText
        }
        this.questions.push(surveyQuestion)
    }
}


//add an answer input
$('body').on('click','.add-answer', function(){
$ul = $(this).parent().find('.answers');
    console.log($(this).children().clone().removeAttr('style'),$ul);
    $(this).children().clone().removeClass('hidden').appendTo($ul);

})

$('body').on('click', '.fa-minus-circle',function(){
    console.log('click');
    $(this).parent().remove();
})
//add question input
$('body').on('click','.add-question',function(){
    $(this).next().clone().removeClass('hidden').appendTo('.survey-container');
    
    
})



$('form').on('submit', handleForm)


async function handleForm(e){
    e.preventDefault()
    const survey = $('.survey-container')
    const title = $('#survey-title').val()
    const instructions = $('#instructions').val()
    const current_survey = new Survey(title, instructions);


    survey.children().each(function(){
        if($(this).attr('id') === "const-container"){
            return
        }
        let question = $(this).find('.survey-question-input').val();
        let answers = [];
        allowText=$(this).find('#allow-text').is(':checked');
        $(this).find('.answer-input').each(function(){
            answer = $(this).val();
            if(answer){
                answers.push(answer);
            }
        })
    current_survey.addQuestion(question,answers,allowText)
    })
    console.log('sending request...', current_survey)
    sendSurvey(current_survey)
}
//add the question and answer data to a global variable
async function sendSurvey(survey){
    console.log(survey)
    axios.post('make-survey/compile',survey).then(function(response){
        window.location.pathname = response.data
    })

}
