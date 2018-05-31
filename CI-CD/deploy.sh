if [ $TRAVIS_BRANCH == 'master' ]
then
  echo "Deploy running."
  ssh -o "StrictHostKeyChecking no" django@homerate.co.uk "cd HomeRate/CI-CD && bash reload.sh && exit"
  echo "Deploy complete."
fi
