$REGION="eu-west-3"
$ACCOUNT_ID="445567115643"
$REPO_NAME="telegram-register-lambda"
$LAMBDA_NAME="telegram-bot"
$IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME`:latest"

docker build --platform linux/amd64 -t $REPO_NAME .
docker tag "$REPO_NAME`:latest" $IMAGE_URI
docker push $IMAGE_URI

Write-Host "4. A atualizar a funcao AWS Lambda..." -ForegroundColor Cyan
aws lambda update-function-code --function-name $LAMBDA_NAME --image-uri $IMAGE_URI --region $REGION

Write-Host "Deploy concluido com sucesso!" -ForegroundColor Green