package twittercrawl;

import java.util.Date;

/**
 *
 * @author 18moh
 */
public class Result {
    public String keyword;
    public long id;
    public String tweet;
    public Date date;
    public String location;
    public int retweets;
    public int likes;
    
    public Result(String keyword, long id, String tweet, Date date, String location, int retweets, int likes){
        this.keyword=keyword;
        this.id=id;
        this.tweet=tweet;
        this.date=date;
        this.location=location;
        this.retweets=retweets;
        this.likes=likes;
    }
    public String toString(){
        return keyword+"|&"+id+"|&"+tweet+"|&"+date+"|&"+location+"|&"+retweets+"|&"+likes;
    }
}
