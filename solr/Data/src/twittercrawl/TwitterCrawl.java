package twittercrawl;

import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;
import java.io.FileWriter;
import java.util.List;
import java.util.ArrayList;

/**
 *
 * @author 18moh
 */
public class TwitterCrawl {
    public static String[] keywords={
        "corona",
        "covid",
        "outbreak",
        "virus",
        "pandemic",
        "epidemic",
        "ban",
        "precaution",
        "contagious",
        "quarantine",
        "health",
        "disease",
        "safe",
        "testing",
        "cough",
        "sick",
        "sickness",
        "cases",
        "recover",
        "patient",
        "china"
    };
    
    public static int keycount=1000;
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        //From Twitter4j documentation, Authorization
        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setDebugEnabled(true)
            .setOAuthConsumerKey("************")
            .setOAuthConsumerSecret("******************")
            .setOAuthAccessToken("**********************")
            .setOAuthAccessTokenSecret("************************");
        TwitterFactory tf = new TwitterFactory(cb.build());
        Twitter twitter = tf.getInstance();
        //

        for(int i=0;i<keywords.length;i++){
            try{
                String key=keywords[i];
                
                ArrayList<Result> r=new ArrayList<Result>();
                
                Query q=new Query(key);
                q.setCount(100);
                q.lang("en");
                
                QueryResult qr=twitter.search(q);                
                List<Status> tweets=qr.getTweets();
                
                while(qr.hasNext() && r.size()<keycount){
                    for(Status s: tweets){
                        if(!s.isRetweet() && r.size()<keycount){
                            Result res=null;
                            if(s.getPlace()!=null){
                                res=new Result(key,s.getId(),s.getText(),s.getCreatedAt(),s.getPlace().getCountry(),s.getRetweetCount(),s.getFavoriteCount());
                            }else{
                                res=new Result(key,s.getId(),s.getText(),s.getCreatedAt(),"N/A",s.getRetweetCount(),s.getFavoriteCount());
                            }
                            
                            r.add(res);
                        }
                    }
                    
                    qr=twitter.search(qr.nextQuery());
                    tweets=qr.getTweets();
                }
                
                System.out.println(key);
                FileWriter f=new FileWriter("key_"+key+".csv",true);
                f.write("keyword|&id|&tweet|&date|&location|&retweets|&likes\n");
                for(Result out:r){
                    f.write(out+"\n");
                }
                f.close();


            }catch(Exception e){
                e.printStackTrace();
            }catch(Error e){
                e.printStackTrace();
            }
        }
    }
    
}
